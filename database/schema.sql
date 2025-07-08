-- Grid table
CREATE TABLE IF NOT EXISTS grid (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Grid region table
CREATE TABLE IF NOT EXISTS grid_region (
    id SERIAL PRIMARY KEY,
    grid_id INTEGER NOT NULL REFERENCES grid(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    UNIQUE(grid_id, name)
);

-- Grid node table
CREATE TABLE IF NOT EXISTS grid_node (
    id SERIAL PRIMARY KEY,
    grid_region_id INTEGER NOT NULL REFERENCES grid_region(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    UNIQUE(grid_region_id, name)
);

-- Measure table
CREATE TABLE IF NOT EXISTS measure (
    grid_node_id INTEGER NOT NULL REFERENCES grid_node(id) ON DELETE CASCADE,
    value DOUBLE PRECISION NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    collected_at TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (grid_node_id, timestamp, collected_at)
);

-- Indexes

-- Efficient filtering by node and timestamp
CREATE INDEX IF NOT EXISTS idx_measure_node_time_collect
    ON measure (grid_node_id, timestamp, collected_at);

-- Fast lookup by timestamp range
CREATE INDEX IF NOT EXISTS idx_measure_timestamp
    ON measure (timestamp);

-- Fast lookup by collected_at timestamp
CREATE INDEX IF NOT EXISTS idx_measure_collected_at
    ON measure (collected_at);

-- Speeds up region-based filtering in grid_node subquery
CREATE INDEX IF NOT EXISTS idx_grid_node_region_id
    ON grid_node (grid_region_id);

-- Optional: helps collected_at + timestamp range filters (without grid_node)
CREATE INDEX IF NOT EXISTS idx_measure_collect_time
    ON measure (collected_at, timestamp);