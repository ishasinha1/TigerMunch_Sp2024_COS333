DROP TABLE IF EXISTS descriptions;

CREATE TABLE descriptions (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    qualitative_description TEXT,
    created_at DATE
);