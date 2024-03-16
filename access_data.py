import auth
import os
import psycopg2

_DATABASE_URL = os.environ['DATABASE_URL']

def insert_meal(calorie_estimate, fat_estimate, protein_estimate, carb_estimate):

    username = auth.authenticate()

    with psycopg2.connect(_DATABASE_URL) as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO user_inputs (username, calories, fat, protein, carbs) VALUES (%s, %s, %s, %s, %s)", (username, calorie_estimate, fat_estimate, protein_estimate, carb_estimate))
                connection.commit()

def fetch_all_data():
    username = auth.authenticate()
    with psycopg2.connect(_DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_inputs WHERE username = %s ORDER BY created_at DESC", (username,))
            return cursor.fetchall()