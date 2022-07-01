import json
import logging
import math
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import emails
import geobuf
import numba
import numpy as np
from emails.template import JinjaTemplate
from fastapi import HTTPException
from geoalchemy2.shape import to_shape
from geojson import Feature, FeatureCollection
from geojson import loads as geojsonloads
from jose import jwt
from numba import njit
from rich import print as print
from shapely.geometry import GeometryCollection, MultiPolygon, Polygon, box
from starlette.responses import Response

from src.core.config import settings
from src.resources.enums import MimeTypes


def send_email_(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST.upper(), "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME.upper()
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email_(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME.upper(), "email": email_to},
    )


email_content_config = {
    "password_recovery": {
        "url": f"{settings.SERVER_HOST}/reset-password?token=",
        "subject": {
            "en": "Password recovery",
            "de": "Passwort zurücksetzen",
        },
        "template_name": "reset_password",
    },
    "activate_new_account": {
        "url": f"{settings.SERVER_HOST}/activate-account?token=",
        "subject": {
            "en": "Activate your account",
            "de": "Demo aktivieren",
        },
        "template_name": "activate_new_account",
    },
    "account_trial_started": {
        "url": "",
        "subject": {
            "en": "Your GOAT demo is ready to use",
            "de": "Ihre GOAT Demo steht bereit",
        },
        "template_name": "account_trial_started",
    },
    "account_expired": {
        "url": "",
        "subject": {"en": "Account expired", "de": "Demo abgelaufen"},
        "template_name": "account_expired",
    },
    "account_expiring": {
        "url": "",
        "subject": {"en": "Account expiring soon", "de": "Demo bald ablaufen"},
        "template_name": "account_expiring",
    },
}


def send_email(
    type: str,
    email_to: str,
    name: str,
    surname: str,
    token: str = "",
    email_language: str = "en",
) -> None:
    if type not in email_content_config:
        raise ValueError(f"Unknown email type {type}")

    subject = email_content_config[type]["subject"][email_language]
    template_str = ""
    available_email_language = "en"
    template_file_name = email_content_config[type]["template_name"]
    link = email_content_config[type]["url"] + token
    if os.path.isfile(
        Path(settings.EMAIL_TEMPLATES_DIR) / f"{template_file_name}_{email_language}.html"
    ):
        available_email_language = email_language
    try:
        with open(
            Path(settings.EMAIL_TEMPLATES_DIR)
            / f"{template_file_name}_{available_email_language}.html"
        ) as f:
            template_str = f.read()
    except OSError:
        print(f"No template for language {available_email_language}")

    send_email_(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME.upper(),
            "name": name,
            "surname": surname,
            "email": email_to,
            "valid_hours": settings.EMAIL_TOKEN_EXPIRE_HOURS,
            "url": link,
        },
    )


def generate_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.API_SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.API_SECRET_KEY, algorithms=["HS256"])
        return decoded_token["sub"]
    except jwt.JWTError:
        return None


def return_geojson_or_geobuf(
    features: Any,
    return_type: str = "geojson",
) -> Any:
    """
    Return geojson or geobuf
    """

    if return_type == "geojson":
        return json.loads(json.dumps(features))
    elif return_type == "geobuf":
        return Response(bytes(geobuf.encode(features)), media_type=MimeTypes.geobuf.value)
    elif return_type == "db_geobuf":
        return Response(bytes(features))
    else:
        raise HTTPException(status_code=400, detail="Invalid return type")


def to_feature_collection(
    sql_result: Any,
    geometry_name: str = "geom",
    geometry_type: str = "wkb",  # wkb | geojson (wkb is postgis geometry which is stored as hex)
    exclude_properties: List = [],
) -> FeatureCollection:
    """
    Generic method to convert sql result to geojson. Geometry field is expected to be in geojson or postgis hex format.
    """
    if not isinstance(sql_result, list):
        sql_result = [sql_result]

    exclude_properties.append(geometry_name)
    features = []
    for row in sql_result:
        if not isinstance(row, dict):
            dict_row = dict(row)
        else:
            dict_row = row
        geometry = None
        if geometry_type == "wkb":
            geometry = to_shape(dict_row[geometry_name])
        elif geometry_type == "geojson":
            geometry = geojsonloads(dict_row[geometry_name])

        features.append(
            Feature(
                id=dict_row.get("gid") or dict_row.get("id") or 0,
                geometry=geometry,
                properties=without_keys(dict_row, exclude_properties),
            )
        )
    return FeatureCollection(features)


def encode_r5_grid(grid_data: Any) -> bytes:
    """
    Encode raster grid data
    """
    return geobuf.encode(grid_data)


def decode_r5_grid(grid_data_buffer: bytes) -> Any:
    """
    Decode R5 grid data
    """
    CURRENT_VERSION = 0
    HEADER_ENTRIES = 7
    HEADER_LENGTH = 9  # type + entries
    TIMES_GRID_TYPE = "ACCESSGR"

    # -- PARSE HEADER
    ## - get header type
    header = {}
    header_data = np.frombuffer(grid_data_buffer, count=8, dtype=np.byte)
    header_type = "".join(map(chr, header_data))
    if header_type != TIMES_GRID_TYPE:
        raise ValueError("Invalid grid type")
    ## - get header data
    header_raw = np.frombuffer(grid_data_buffer, count=HEADER_ENTRIES, offset=8, dtype=np.int32)
    version = header_raw[0]
    if version != CURRENT_VERSION:
        raise ValueError("Invalid grid version")
    header["zoom"] = header_raw[1]
    header["west"] = header_raw[2]
    header["north"] = header_raw[3]
    header["width"] = header_raw[4]
    header["height"] = header_raw[5]
    header["depth"] = header_raw[6]
    header["version"] = version

    # -- PARSE DATA --
    gridSize = header["width"] * header["height"]
    # - skip the header
    data = np.frombuffer(
        grid_data_buffer,
        offset=HEADER_LENGTH * 4,
        count=gridSize * header["depth"],
        dtype=np.int32,
    )
    # - reshape the data
    data = data.reshape(header["depth"], gridSize)
    reshaped_data = np.array([])
    for i in range(header["depth"]):
        reshaped_data = np.append(reshaped_data, data[i].cumsum())
    data = reshaped_data
    # - decode metadata
    raw_metadata = np.frombuffer(
        grid_data_buffer,
        offset=(HEADER_LENGTH + header["width"] * header["height"] * header["depth"]) * 4,
        dtype=np.int8,
    )
    metadata = json.loads(raw_metadata.tostring())

    return header | metadata | {"data": data, "errors": [], "warnings": []}


@njit
def compute_single_value_surface(width, height, depth, data, percentile) -> Any:
    """
    Compute single value surface
    """
    if data == None or width == None or height == None or depth == None:
        return None
    grid_size = width * height
    surface = np.empty(grid_size)
    TRAVEL_TIME_PERCENTILES = [5, 25, 50, 75, 95]
    percentile_index = 0
    closest_diff = math.inf
    for index, p in enumerate(TRAVEL_TIME_PERCENTILES):
        current_diff = abs(p - percentile)
        if current_diff < closest_diff:
            percentile_index = index
            closest_diff = current_diff
    for y in np.arange(height):
        for x in np.arange(width):
            index = y * width + x
            if (
                x >= 0
                and x < width
                and y >= 0
                and y < height
                and percentile_index >= 0
                and percentile_index < depth
            ):
                coord = data[(percentile_index * grid_size) + (y * width) + x]
            else:
                coord = math.inf

            surface[index] = coord
    return surface


@njit
def amenity_r5_grid_intersect(
    west,
    north,
    width,
    surface,
    get_population_sum_pixel,
    get_population_sum_population,
    get_poi_one_entrance_sum_pixel,
    get_poi_one_entrance_sum_category,
    get_poi_one_entrance_sum_cnt,
    get_poi_more_entrance_sum_pixel,
    get_poi_more_entrance_sum_category,
    get_poi_more_entrance_sum_name,
    get_poi_more_entrance_sum_cnt,
    MAX_TIME=120,
):
    """
    Return a list of amenity count for every minute
    """
    population_grid_count = np.zeros(MAX_TIME)
    # - loop population
    for idx, pixel in enumerate(get_population_sum_pixel):
        pixel_x = pixel[1]
        pixel_y = pixel[0]
        x = pixel_x - west
        y = pixel_y - north
        width = width
        index = y * width + x
        time_cost = surface[index]
        if time_cost < 2147483647:
            population = get_population_sum_population[idx]
            population_grid_count[int(time_cost)] += population
    population_grid_count = np.cumsum(population_grid_count)

    # - loop poi_one_entrance
    poi_one_entrance_list = numba.typed.List()
    poi_one_entrance_grid_count = numba.typed.List()
    for idx, pixel in enumerate(get_poi_one_entrance_sum_pixel):
        pixel_x = pixel[1]
        pixel_y = pixel[0]
        x = pixel_x - west
        y = pixel_y - north
        width = width
        index = y * width + x
        category = get_poi_one_entrance_sum_category[idx]

        if category not in poi_one_entrance_list:
            poi_one_entrance_list.append(category)
            poi_one_entrance_grid_count.append(np.zeros(MAX_TIME))

        time_cost = surface[index]
        if time_cost < 2147483647:
            count = get_poi_one_entrance_sum_cnt[idx]
            poi_one_entrance_grid_count[poi_one_entrance_list.index(category)][
                int(time_cost)
            ] += count

    for index, value in enumerate(poi_one_entrance_grid_count):
        poi_one_entrance_grid_count[index] = np.cumsum(value)

    # - loop poi_more_entrance
    visited_more_entrance_categories = numba.typed.List()
    poi_more_entrance_list = numba.typed.List()
    poi_more_entrance_grid_count = numba.typed.List()
    for idx, pixel in enumerate(get_poi_more_entrance_sum_pixel):
        pixel_x = pixel[1]
        pixel_y = pixel[0]
        x = pixel_x - west
        y = pixel_y - north
        width = width
        index = y * width + x
        category = get_poi_more_entrance_sum_category[idx]
        name = get_poi_more_entrance_sum_name[idx]

        if category not in poi_more_entrance_list:
            poi_more_entrance_list.append(category)
            poi_more_entrance_grid_count.append(np.zeros(MAX_TIME))

        time_cost = surface[index]
        category_name = f"{category}_{name}"
        if time_cost < 2147483647 and category_name not in visited_more_entrance_categories:
            count = get_poi_more_entrance_sum_cnt[idx]
            poi_more_entrance_grid_count[poi_more_entrance_list.index(category)][
                int(time_cost)
            ] += count
            visited_more_entrance_categories.append(category_name)

    for index, value in enumerate(poi_more_entrance_grid_count):
        poi_more_entrance_grid_count[index] = np.cumsum(value)

    return (
        population_grid_count,
        poi_one_entrance_list,
        poi_one_entrance_grid_count,
        poi_more_entrance_list,
        poi_more_entrance_grid_count,
    )


@njit
def z_scale(z):
    """
    2^z represents the tile number. Scale that by the number of pixels in each tile.
    """
    PIXELS_PER_TILE = 256
    return 2 ** z * PIXELS_PER_TILE


@njit
def pixel_to_longitude(pixel_x, zoom):
    """
    Convert pixel x coordinate to longitude
    """
    return (pixel_x / z_scale(zoom)) * 360 - 180


@njit
def pixel_to_latitude(pixel_y, zoom):
    """
    Convert pixel y coordinate to latitude
    """
    lat_rad = math.atan(math.sinh(math.pi * (1 - (2 * pixel_y) / z_scale(zoom))))
    return lat_rad * 180 / math.pi


@njit
def coordinate_from_pixel(pixel, zoom):
    """
    Convert pixel coordinate to longitude and latitude
    """
    return {
        "lat": pixel_to_latitude(pixel["y"], zoom),
        "lon": pixel_to_longitude(pixel["x"], zoom),
    }


def katana(geometry, threshold, count=0):
    """Split a Polygon into two parts across it's shortest dimension"""
    bounds = geometry.bounds
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    if max(width, height) <= threshold or count == 250:
        # either the polygon is smaller than the threshold, or the maximum
        # number of recursions has been reached
        return [geometry]
    if height >= width:
        # split left to right
        a = box(bounds[0], bounds[1], bounds[2], bounds[1] + height / 2)
        b = box(bounds[0], bounds[1] + height / 2, bounds[2], bounds[3])
    else:
        # split top to bottom
        a = box(bounds[0], bounds[1], bounds[0] + width / 2, bounds[3])
        b = box(bounds[0] + width / 2, bounds[1], bounds[2], bounds[3])
    result = []
    for d in (
        a,
        b,
    ):
        c = geometry.intersection(d)
        if not isinstance(c, GeometryCollection):
            c = [c]
        for e in c:
            if isinstance(e, (Polygon, MultiPolygon)):
                result.extend(katana(e, threshold, count + 1))
    if count > 0:
        return result
    # convert multipart into singlepart
    final_result = []
    for g in result:
        if isinstance(g, MultiPolygon):
            final_result.extend(g)
        else:
            final_result.append(g)
    return final_result


def without_keys(d, keys):
    """
    Omit keys from a dict
    """
    return {x: d[x] for x in d if x not in keys}


def delete_file(file_path: str) -> None:
    """Delete file from disk."""
    try:
        os.remove(file_path)
    except OSError as e:
        pass


def delete_dir(dir_path: str) -> None:
    """Delete file from disk."""
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        pass


def clean_unpacked_zip(dir_path: str, zip_path: str) -> None:
    """Delete unpacked zip file and directory."""
    delete_dir(dir_path)
    delete_file(zip_path)


def print_hashtags():
    print(
        "#################################################################################################################"
    )


def print_info(message: str):
    print(f"[bold green]INFO[/bold green]: {message}")


def print_warning(message: str):
    print(f"[bold red]WARNING[/bold red]: {message}")
