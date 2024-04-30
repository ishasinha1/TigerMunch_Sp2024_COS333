-- Generate and insert synthetic data
DO $$
DECLARE
    i int := 0;
    entry_date date := '2024-04-30'; -- starting date
BEGIN
    WHILE i < 35 LOOP
        INSERT INTO user_inputs (username, calories, fat, protein, carbs, created_at)
        VALUES (
            'is4684',
            floor(random() * (3000 - 1500 + 1) + 1500), -- Random calories between 1500 and 3000
            floor(random() * (300 - 100 + 1) + 100),    -- Random fat between 100 and 300
            floor(random() * (300 - 100 + 1) + 100),    -- Random protein between 100 and 300
            floor(random() * (300 - 100 + 1) + 100),    -- Random carbs between 100 and 300
            entry_date
        );
        entry_date := entry_date - interval '1 day';
        i := i + 1;
    END LOOP;
END $$;
