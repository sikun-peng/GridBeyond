import logging
from datetime import datetime, timedelta, timezone
import random
from app.postgres_client import (
    insert_static_data,
    get_all_nodes,
    insert_measurement_bulk
)

logger = logging.getLogger(__name__)

def generate_time_series_data():
    node_ids = get_all_nodes()
    base_time = datetime.utcnow().replace(tzinfo=timezone.utc, minute=0, second=0, microsecond=0)
    start_target = base_time + timedelta(hours=1)
    end_target = base_time + timedelta(days=7)
    
    data = []
    for node_id in node_ids:
        target_time = start_target
        while target_time <= end_target:
            collected_at = base_time
            while collected_at <= target_time:
                value = round(random.uniform(90, 110), 2)
                data.append((node_id, value, target_time, collected_at))
                collected_at += timedelta(hours=1)
            target_time += timedelta(hours=1)
    
    MAX_ROWS = 300000
    data = data[:MAX_ROWS]
    logger.info("Prepared %d records", len(data))

    batch_size = 1000
    for i in range(0, len(data), batch_size):
        insert_measurement_bulk(data[i:i+batch_size])
        logger.info("Inserted batch %d", (i // batch_size) + 1)

def main():
    logger.info("Inserting static data...")
    insert_static_data()
    logger.info("Generating measurements...")
    generate_time_series_data()
    logger.info("Done!")

if __name__ == "__main__":
    main()