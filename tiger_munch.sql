DROP TABLE IF EXISTS user_inputs;

CREATE TABLE user_inputs (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    calories DECIMAL,
    fat DECIMAL,
    protein DECIMAL,
    carbs DECIMAL,
    created_at DATE
);

DROP TABLE IF EXISTS user_data;

CREATE TABLE user_data (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    daily_calorie_goal DECIMAL,
    daily_fat_goal DECIMAL,
    daily_protein_goal DECIMAL,
    daily_carb_goal DECIMAL
);

