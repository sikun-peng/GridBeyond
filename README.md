# GridBeyond

This submission contains a PostgreSQL-backed Python exercise for mocking time-series data across Grid, Region and Node

## Features

- Relational schema with Grid -> Region -> Node hierarchy
- Timeseries data model supporting value evolution
- API to query:
  - Latest value for each timestamp
  - Value as collected at a specific time
- Script to insert 1 week of sample data

## Setup Instructions 

### 1. Install Requirements
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```


### 2. Setup PostgreSQL database:

```bash
createdb gridbeyond
psql gridbeyond -f database/schemas.sql

```

### 3. Generate data:
```bash
python3 -m database.data_migration
```

### 4.  Run API
```bash
python3 -m uvicorn api.main:app --reload
```

### 5. Example rest calls

Swagger - http://localhost:8000/docs

```bash
curl -X POST "http://localhost:8000/latest_measures" \
  -H "Content-Type: application/json" \
  -d '{
    "start_datetime": "2025-07-07T00:00:00Z",
    "end_datetime": "2025-07-08T00:00:00Z",
    "region_id": 3
  }'
```

```bash
curl -X POST "http://localhost:8000/measures_at_collection" \
  -H "Content-Type: application/json" \
  -d '{
        "start_datetime": "2025-07-07T00:00:00Z",
        "end_datetime": "2025-07-14T00:00:00Z",
        "collected_datetime": "2025-07-07T17:00:00Z",
        "node_id": 3,
        "limit": 20,
        "offset": 10
      }'
```