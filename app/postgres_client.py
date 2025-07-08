import logging
import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from datetime import datetime
from .postgres_config import PostgresConfig  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
pg_config = PostgresConfig()

@contextmanager
def database_connection():
    """Context manager for database connections"""
    conn = psycopg2.connect(
        dbname=pg_config.db_name,
        user=pg_config.user,
        password=pg_config.password,
        host=pg_config.host,
        port=pg_config.port
    )
    try:
        yield conn
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def execute_query(query, params=None, fetch=False):
    """Generic query executor"""
    logger.info("Executing SQL query...")
    logger.info("Query: %s", query)
    logger.info("Parameters: %s", params)
    with database_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if fetch:
                return cur.fetchall()
            conn.commit()

def get_latest_measures(start_dt, end_dt, grid_id=None, region_id=None, node_id=None, limit=1000, offset=0):
    filters = ["timestamp BETWEEN %s AND %s"]
    params = [start_dt, end_dt]

    if node_id:
        filters.append("grid_node_id = %s")
        params.append(node_id)
    elif region_id:
        filters.append("grid_node_id IN (SELECT id FROM grid_node WHERE grid_region_id = %s)")
        params.append(region_id)
    elif grid_id:
        filters.append("""grid_node_id IN (
            SELECT gn.id FROM grid_node gn
            JOIN grid_region gr ON gn.grid_region_id = gr.id
            WHERE gr.grid_id = %s
        )""")
        params.append(grid_id)

    query = f"""
        SELECT DISTINCT ON (grid_node_id, timestamp)
            grid_node_id, timestamp, value
        FROM measure
        WHERE {' AND '.join(filters)}
        ORDER BY grid_node_id, timestamp, collected_at DESC
        LIMIT %s OFFSET %s
    """
    params.extend([limit, offset])
    return execute_query(query, params, fetch=True)

def get_measures_at_collection(start_dt, end_dt, collected_dt, grid_id=None, region_id=None, node_id=None, limit=1000, offset=0):
    if collected_dt.tzinfo is not None:
        collected_dt = collected_dt.replace(tzinfo=None)
    query = """
        SELECT m.grid_node_id, m.timestamp, m.value
        FROM measure m
        JOIN grid_node n ON m.grid_node_id = n.id
        JOIN grid_region r ON n.grid_region_id = r.id
        JOIN grid g ON r.grid_id = g.id
        WHERE m.timestamp BETWEEN %s AND %s
        AND m.collected_at::timestamp = %s
    """
    params = [start_dt, end_dt, collected_dt]

    if grid_id:
        query += " AND g.id = %s"
        params.append(grid_id)
    if region_id:
        query += " AND r.id = %s"
        params.append(region_id)
    if node_id:
        query += " AND m.grid_node_id = %s"
        params.append(node_id)

    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    return execute_query(query, params, fetch=True)

def get_all_nodes() -> list:
    """Get all grid node IDs"""
    return [row[0] for row in execute_query("SELECT id FROM grid_node", fetch=True)]

def insert_static_data():
    """Insert static grid hierarchy data"""
    # Insert grids
    for grid in ['Grid1', 'Grid2', 'Grid3']:
        execute_query(
            "INSERT INTO grid (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", 
            (grid,)
        )
    
    # Insert 3 regions per grid
    for grid_id in range(1, 4):
        for region_num in range(1, 4):
            execute_query(
                "INSERT INTO grid_region (grid_id, name) VALUES (%s, %s) "
                "ON CONFLICT (grid_id, name) DO NOTHING",
                (grid_id, f"Region{region_num}")
            )
    
    # Insert 3 nodes per region
    for region_id in range(1, 10):
        for node_num in range(1, 4):
            execute_query(
                "INSERT INTO grid_node (grid_region_id, name) VALUES (%s, %s) "
                "ON CONFLICT (grid_region_id, name) DO NOTHING",
                (region_id, f"Node{node_num}")
            )

def insert_measurement_bulk(data: list):
    """Bulk insert measurements"""
    query = """
        INSERT INTO measure (grid_node_id, value, timestamp, collected_at)
        VALUES %s
        ON CONFLICT (grid_node_id, timestamp, collected_at) DO NOTHING
    """
    with database_connection() as conn:
        with conn.cursor() as cur:
            psycopg2.extras.execute_values(
                cur, query, data, template="(%s, %s, %s, %s)"
            )
            conn.commit()