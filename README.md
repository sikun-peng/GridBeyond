# GridBeyond

This project demonstrates a PostgreSQL-backed Python application that simulates and queries time-series data across a hierarchical energy grid structure: Grid → Region → Node.

## Features

- Normalized schema representing grid infrastructure: Grid -> Region -> Node hierarchy
- Time-series data model supporting historical value snapshots (timestamp) and data collection time (collected_at)
- FastAPI-based endpoints:
  - Query latest values across grid nodes
  - Retrieve values as collected at a specific timestamp
- Script to generate 1 week of sample data

## Setup Instructions 

### 1. Install Requirements:
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

### 3. Generate Sample Time-Series Data:
```bash
python3 -m database.data_migration
```

### 4. Start the API Server:
```bash
python3 -m uvicorn api.main:app --reload
```


## API Usage

### Interactive docs available at: http://localhost:8000/docs

### Example: Get Latest Measures by Region

```bash
curl -X POST "http://localhost:8000/latest_measures" \
  -H "Content-Type: application/json" \
  -d '{
    "start_datetime": "2025-07-07T00:00:00Z",
    "end_datetime": "2025-07-08T00:00:00Z",
    "region_id": 3
  }'
```

### Example: Get Measures at Collection Time

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