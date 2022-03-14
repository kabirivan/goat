from datetime import datetime
from enum import Enum
from typing import Dict, Iterable, List, Optional, Union

from geojson_pydantic.features import FeatureCollection
from pydantic import BaseModel, Field, create_model

from src.db import models


class ScenarioBase(BaseModel):
    scenario_id: int


class ScenarioImport(ScenarioBase):
    user_id: int
    layer_name: str
    payload: FeatureCollection

    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "scenario_id": 6,
                "layer_name": "ways",
                "payload": {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "LineString",
                                "coordinates": [
                                    [7.850605211, 47.995588854000005],
                                    [7.850990133, 47.99593471899999],
                                    [7.851685883999999, 47.99564569199998],
                                ],
                            },
                            "properties": {
                                "lit": "null",
                                "foot": "null",
                                "bicycle": "null",
                                "surface": "asphalt",
                                "way_type": "bridge",
                                "edit_type": "new",
                                "wheelchair": "yes",
                                "original_id": "null",
                                "street_category": "null",
                            },
                            "id": 1,
                        }
                    ],
                },
            }
        }


class ScenarioDelete(ScenarioBase):
    layer_name: str
    deleted_feature_ids: List[int]
    drew_fid: int

    class Config:
        schema_extra = {
            "example": {
                "scenario_id": 1,
                "layer_name": "pois",
                "deleted_feature_ids": [1, 2, 3],
                "drew_fid": 14,
            }
        }


# -----------------------------------------------------------------------------
class ScenarioLayersEnum(Enum):
    """Scenario Layers Enums."""

    ways = "ways"
    pois = "pois"
    buildings = "buildings"


class ScenarioLayerFeatureEnum(Enum):
    """Scenario Layer Feature Delete Enums."""

    way_modified = "way_modified"
    poi_modified = "poi_modified"
    building_modified = "building_modified"
    population_modified = "population_modified"


class ScenarioLayersNoPoisEnum(Enum):
    """Scenario Layers without POIS."""

    edge = "edge"
    way_modified = "way_modified"
    building = "building"
    building_modified = "building_modified"
    population = "population"
    population_modified = "population_modified"


class WayModifiedTypeEnum(str, Enum):
    bridge = "bridge"
    road = "road"


class WayModifiedWheelchairEnum(str, Enum):
    yes = "yes"
    no = "no"


class WayModifiedSurfaceEnum(str, Enum):
    asphalt = "asphalt"
    cobblestone = "cobblestone"
    fine_gravel = "fine_gravel"
    gravel = "gravel"
    grass = "grass"
    unpaved = "unpaved"


class BuildingModifiedTypeEnum(str, Enum):
    residential = "residential"
    commercial = "commercial"
    public = "public"


class ScenarioCreate(BaseModel):
    scenario_name: str


class ScenarioUpdate(BaseModel):
    scenario_name: str


# ----------- SCENARIO FEATURE CRUD SCHEMAS------------------------


class ScenarioFeatureCreateBase(BaseModel):
    geom: str


class ScenarioFeatureUpdateBase(BaseModel):
    id: int
    geom: Optional[str]


class ScenarioWaysModifiedCreate(ScenarioFeatureCreateBase):
    way_id: Optional[int] = None  # specified if the feature is an existing way from edge table
    surface: WayModifiedSurfaceEnum
    way_type: WayModifiedTypeEnum
    wheelchair: WayModifiedWheelchairEnum
    class_id: Optional[int] = 100  # specified if the feature is an existing way from edge table

    class Config:
        extra = "forbid"
        schema_extra = {
            "client_config": {
                "name": "ways",
                "editDataType": "GeoJSON",
                "editGeometry": ["LineString"],
                "modifyAttributes": True,
                "displayInLayerList": False,
                "enableFileUpload": False,
            },
        }


class ScenarioWaysModifiedUpdate(ScenarioFeatureUpdateBase):
    surface: Optional[WayModifiedSurfaceEnum]
    way_type: Optional[WayModifiedTypeEnum]
    wheelchair: Optional[WayModifiedWheelchairEnum]
    class_id: Optional[int]

    class Config:
        extra = "forbid"


class ScenarioBuildingsModifiedCreate(ScenarioFeatureCreateBase):
    building_id: Optional[
        int
    ] = None  # specified if the feature is an existing building from buildings table
    building: BuildingModifiedTypeEnum
    building_levels: int
    building_levels_residential: int
    population: int

    class Config:
        extra = "forbid"
        schema_extra = {
            "client_config": {
                "name": "buildings",
                "editDataType": "GeoJSON",
                "editGeometry": ["Polygon", "MultiPolygon"],
                "canModifyGeom": True,
                "modifyAttributes": True,
                "displayInLayerList": False,
                "enableFileUpload": True,
            },
        }


class ScenarioBuildingsModifiedUpdate(ScenarioFeatureUpdateBase):
    building: Optional[BuildingModifiedTypeEnum]
    building_levels: Optional[int]
    building_levels_residential: Optional[int]
    population: Optional[int]

    class Config:
        extra = "forbid"


class ScenarioPoisModifiedCreate(ScenarioFeatureCreateBase):
    uid: Optional[int] = None  # specified if the feature is an existing poi from pois table
    name: str
    amenity: str  # checked if amenity exists for the user

    class Config:
        extra = "forbid"
        schema_extra = {
            "client_config": {
                "name": "pois",
                "editDataType": "GeoJSON",
                "editGeometry": ["Point"],
                "displayInLayerList": False,
                "enableFileUpload": False,
            },
        }


class ScenarioPoisModifiedUpdate(ScenarioFeatureUpdateBase):
    name: Optional[str]
    amenity: Optional[str]

    class Config:
        extra = "forbid"


class ScenarioPopulationModifiedCreate(ScenarioFeatureCreateBase):
    building_modified_id: int

    class Config:
        extra = "forbid"
        title = "population"


class ScenarioPopulationModifiedUpdate(ScenarioFeatureUpdateBase):
    class Config:
        extra = "forbid"


class ScenarioFeatureCreate(BaseModel):
    features: List[
        Union[
            ScenarioWaysModifiedCreate,
            ScenarioBuildingsModifiedCreate,
            ScenarioPoisModifiedCreate,
            ScenarioPopulationModifiedCreate,
        ]
    ]


class ScenarioFeatureUpdate(BaseModel):
    features: List[
        Union[
            ScenarioWaysModifiedUpdate,
            ScenarioBuildingsModifiedUpdate,
            ScenarioPoisModifiedUpdate,
            ScenarioPopulationModifiedUpdate,
        ]
    ]


"""
Request payloads
"""
request_examples = {
    "create": {"scenario_name": "test"},
    "update": {"scenario_name": "test_updated"},
    "update_deleted_features": [1, 2, 3],
    "read_features": {
        "scenario_id": 1,
        "layer_name": "edge",
        "intersect": "POLYGON((11.55947247425152 48.15680551331815,11.559310821465383 48.15790039566741,11.558832075332894 48.15895318026625,11.558054633799436 48.159923412979424,11.557008373507147 48.16077381397483,11.555733501652313 48.161471709503445,11.554279010845356 48.161990286516016,11.552700796352298 48.162309622055574,11.551059508071036 48.162417448022694,11.549418219789775 48.162309622055574,11.547840005296717 48.161990286516016,11.546385514489758 48.161471709503445,11.545110642634924 48.16077381397483,11.544064382342636 48.159923412979424,11.543286940809178 48.15895318026625,11.54280819467669 48.15790039566741,11.542646541890553 48.15680551331815,11.54280819467669 48.155710607603396,11.543286940809178 48.15465775646527,11.544064382342636 48.153687424168936,11.545110642634924 48.15283690570729,11.546385514489758 48.152138892712344,11.547840005296717 48.15162021611667,11.549418219789775 48.151300814037825,11.551059508071036 48.15119296470522,11.552700796352298 48.151300814037825,11.554279010845356 48.15162021611667,11.555733501652313 48.152138892712344,11.557008373507147 48.15283690570729,11.558054633799436 48.153687424168936,11.558832075332894 48.15465775646527,11.559310821465383 48.155710607603396,11.55947247425152 48.15680551331815))",
    },
    "delete_feature": {
        "scenario_id": 1,
        "layer_name": "way_modified",
        "feature_id": 1,
    },
    "create_feature": {
        "scenario_id": 1,
        "layer_name": "way_modified",
        "payload": {
            "ways_modified": {
                "summary": "Create a new way",
                "value": {
                    "features": [
                        {
                            "class_id": 113,
                            "way_type": "bridge",
                            "surface": "asphalt",
                            "wheelchair": "yes",
                            "lit": None,
                            "geom": "LINESTRING(11.510148251443228 48.1643284471769,11.5112867863764 48.1634171605524,11.513123622735256 48.16285012959281,11.515264068409625 48.162475480698475,11.515598038656687 48.16323490128468,11.516660671260983 48.163862680480435)",
                        }
                    ]
                },
            },
            "buildings_modified": {
                "summary": "Create a new building",
                "value": {
                    "features": [
                        {
                            "building_id": None,
                            "building": "residential",
                            "building_levels": 3,
                            "building_levels_residential": 3,
                            "population": 0,
                            "geom": "POLYGON((11.609135868999951 48.1456709710543,11.609658256585695 48.14557960155892,11.6095458739245 48.14529354216867,11.609023486338758 48.145384912173284,11.609135868999951 48.1456709710543))",
                        }
                    ]
                },
            },
            "pois_modified": {
                "summary": "Create a new poi",
                "value": {
                    "features": [
                        {
                            "uid": "poi_1",
                            "name": "poi_1",
                            "amenity": "bar",
                            "geom": "POINT(11.610550880033179 48.14586047763734)",
                        }
                    ]
                },
            },
            "population_modified": {
                "summary": "Create a new population",
                "value": {
                    "features": [
                        {
                            "building_modified_id": 1,
                            "geom": "POINT(11.609333666241154 48.145444239044565)",
                        }
                    ]
                },
            },
        },
    },
    "update_feature": {
        "scenario_id": 1,
        "layer_name": "way_modified",
        "payload": {
            "ways_modified": {
                "summary": "Update way",
                "value": {
                    "features": [
                        {
                            "id": 1,
                            "class_id": 113,
                            "way_type": "bridge",
                            "surface": "asphalt",
                            "wheelchair": "yes",
                            "geom": "LINESTRING(11.510148251443228 48.1643284471769,11.5112867863764 48.1634171605524,11.513123622735256 48.16285012959281,11.515264068409625 48.162475480698475,11.515598038656687 48.16323490128468,11.516660671260983 48.163862680480435)",
                        }
                    ]
                },
            },
            "buildings_modified": {
                "summary": "Update building",
                "value": {
                    "features": [
                        {
                            "id": 1,
                            "building": "residential",
                            "building_levels": 3,
                            "building_levels_residential": 3,
                            "population": 0,
                            "geom": "POLYGON((11.609135868999951 48.1456709710543,11.609658256585695 48.14557960155892,11.6095458739245 48.14529354216867,11.609023486338758 48.145384912173284,11.609135868999951 48.1456709710543))",
                        }
                    ]
                },
            },
            "pois_modified": {
                "summary": "Update poi",
                "value": {
                    "features": [
                        {
                            "id": 1,
                            "name": "poi_1",
                            "amenity": "bar",
                            "geom": "POINT(11.610550880033179 48.14586047763734)",
                        }
                    ]
                },
            },
            "population_modified": {
                "summary": "Update population",
                "value": {
                    "features": [
                        {
                            "id": 1,
                            "geom": "POINT(11.609333666241154 48.145444239044565)",
                        }
                    ]
                },
            },
        },
    },
}
