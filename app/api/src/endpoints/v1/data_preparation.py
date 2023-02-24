import json
import linecache
import os
import tracemalloc

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

# from src.crud import crud_compute_heatmap_old
from src.crud.crud_compute_heatmap import CRUDComputeHeatmap
from src.db import models
from src.endpoints import deps
from src.endpoints.v1 import data_preparation_connector, data_preparation_tasks
from src.schemas import data_preparation as schemas

router = APIRouter()

def display_top(snapshot, key_type='lineno', limit=3):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


@router.post("/travel-time-matrices")
async def get_bulk_ids_for_study_area(
    *,
    db: AsyncSession = Depends(deps.get_db),
    current_super_user: models.User = Depends(deps.get_current_active_superuser),
    parameters: schemas.BulkIdParameters = Body(..., example=schemas.BulkIdParametersExample)):
    
    crud_compute_heatmap = CRUDComputeHeatmap(db, current_super_user)
    return await crud_compute_heatmap.get_bulk_ids(**parameters.dict())

@router.post("/traveltime-matrices")
async def create_traveltime_matrices(
    *,
    current_super_user: models.User = Depends(deps.get_current_active_superuser),
    parameters: schemas.OpportunityMatrixParameters2 = Body(..., example=schemas.OpportunityMatrixParametersExample)):
    parameters = json.loads(parameters.json())
    parameters2 = parameters.copy()
    current_super_user = json.loads(current_super_user.json())
    for bulk_id in parameters["bulk_id"]:
        parameters2["bulk_id"] = bulk_id
        #await data_preparation_connector.create_traveltime_matrices_async(current_super_user, parameters2)
        data_preparation_tasks.create_traveltime_matrices_sync.delay(current_super_user, parameters2)
    return JSONResponse("Ok")

@router.post("/traveltime-matrices-debug")
async def create_traveltime_matrices(
    *,
    current_super_user: models.User = Depends(deps.get_current_active_superuser),
    parameters: schemas.OpportunityMatrixParameters2 = Body(..., example=schemas.OpportunityMatrixParametersExample)
    ):
    parameters = json.loads(parameters.json())
    parameters2 = parameters.copy()
    current_super_user = json.loads(current_super_user.json())
    for bulk_id in parameters["bulk_id"]:
        parameters2["bulk_id"] = bulk_id
        await data_preparation_connector.create_traveltime_matrices_async(current_super_user, parameters2)
        #data_preparation_tasks.create_traveltime_matrices_sync.delay(current_super_user, parameters2)
    return JSONResponse("Ok")


@router.post("/opportunity-matrices")
async def create_opportunity_matrices(
    *,
    current_super_user: models.User = Depends(deps.get_current_active_superuser),
    parameters: schemas.OpportunityMatrixParameters2 = Body(..., example=schemas.OpportunityMatrixParametersExample)):
    parameters = json.loads(parameters.json())
    parameters2 = parameters.copy()
    current_super_user = json.loads(current_super_user.json())
    for bulk_id in parameters["bulk_id"]:
        parameters2["bulk_id"] = bulk_id
        # data_preparation_tasks.create_opportunity_matrices_sync.delay(current_super_user, parameters2)
        tracemalloc.start()
        await data_preparation_connector.create_opportunity_matrices_async(current_super_user, parameters2)
        snapshot = tracemalloc.take_snapshot()
        display_top(snapshot)
    return JSONResponse("Ok")


@router.post("/connectivity-matrices")
async def create_connectivity_matrices(
    *,
    current_super_user: models.User = Depends(deps.get_current_active_superuser),
    parameters: schemas.ConnectivityMatrixParameters = Body(..., example=schemas.ConnectivityMatrixExample)):
    parameters = json.loads(parameters.json())
    current_super_user = json.loads(current_super_user.json())
    # data_preparation_tasks.create_connectivity_matrices_sync.delay(current_super_user, parameters2)
    await data_preparation_connector.create_connectivity_matrices_async(current_super_user, parameters)
    return JSONResponse("Ok")