-- init-scripts/init.sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(20) PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    embedding VECTOR(384)
);