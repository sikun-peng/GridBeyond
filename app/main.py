from fastapi import FastAPI, HTTPException
from . import schemas
from .postgres_client import (
    get_latest_measures,
    get_measures_at_collection
)
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = FastAPI()

@app.post("/latest_measures", response_model=list[schemas.MeasureResponse])
def get_latest_measures_api(request: schemas.DateRangeRequest):
    try:
        results = get_latest_measures(
            request.start_datetime,
            request.end_datetime,
            request.grid_id,
            request.region_id,
            request.node_id,
            request.limit,
            request.offset
        )
        return [
            {"grid_node_id": row[0], "timestamp": row[1], "value": row[2]}
            for row in results
        ]
    except Exception as e:
        raise HTTPException(500, f"Database error: {e}")


@app.post("/measures_at_collection", response_model=list[schemas.MeasureResponse])
def get_measures_at_collection_api(request: schemas.CollectionTimeRequest):
    try:
        results = get_measures_at_collection(
            request.start_datetime,
            request.end_datetime,
            request.collected_datetime,
            request.grid_id,
            request.region_id,
            request.node_id,
            request.limit,
            request.offset
        )
        return [
            {"grid_node_id": row[0], "timestamp": row[1], "value": row[2]}
            for row in results
        ]
    except Exception as e:
        raise HTTPException(500, f"Database error: {e}")