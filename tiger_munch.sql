DROP TABLE IF EXISTS user_inputs;

CREATE TABLE user_inputs (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    calories DECIMAL,
    fat DECIMAL,
    protein DECIMAL,
    carbs DECIMAL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

