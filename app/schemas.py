from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DateRangeRequest(BaseModel):
    start_datetime: datetime
    end_datetime: datetime
    grid_id: Optional[int] = None
    region_id: Optional[int] = None
    node_id: Optional[int] = None
    limit: Optional[int] = 1000
    offset: Optional[int] = 0

class CollectionTimeRequest(BaseModel):
    start_datetime: datetime
    end_datetime: datetime
    collected_datetime: datetime
    grid_id: Optional[int] = None
    region_id: Optional[int] = None
    node_id: Optional[int] = None
    limit: Optional[int] = 1000
    offset: Optional[int] = 0

class MeasureResponse(BaseModel):
    grid_node_id: int
    timestamp: datetime
    value: float