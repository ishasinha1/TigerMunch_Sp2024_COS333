import auth
import os
import psycopg2
from datetime import datetime
import request_handler

_DATABASE_URL = os.environ['DATABASE_URL']

def insert_meal(calorie_estimate, fat_estimate, protein_estimate, carb_estimate):
    username = auth.authenticate()
    current_date = datetime.now().date() 
    # current_date = datetime(2023, 12, 20)

    with psycopg2.connect(_DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT calories, fat, protein, carbs FROM user_inputs WHERE username = %s AND created_at = %s", (username, current_date))
            existing = cursor.fetchone()

            if existing:
                # Entry exists, calculate new totals
                new_calories = calorie_estimate + float(existing[0])
                new_fat = fat_estimate + float(existing[1])
                new_protein = protein_estimate + float(existing[2])
                new_carbs = carb_estimate + float(existing[3])

                # Update the entry with new totals
                cursor.execute("UPDATE user_inputs SET calories = %s, fat = %s, protein = %s, carbs = %s WHERE username = %s AND created_at = %s", 
                               (new_calories, new_fat, new_protein, new_carbs, username, current_date))
            else:
                # Entry does not exist, insert a new one
                cursor.execute("INSERT INTO user_inputs (username, calories, fat, protein, carbs, created_at) VALUES (%s, %s, %s, %s, %s, %s)", 
                               (username, calorie_estimate, fat_estimate, protein_estimate, carb_estimate, current_date))
                        
            connection.commit()

def fetch_all_data():
    username = auth.authenticate()
    with psycopg2.connect(_DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_inputs WHERE username = %s ORDER BY created_at DESC", (username,))
            return cursor.fetchall()

def fetch_page_data(limit):
    username = auth.authenticate()
    with psycopg2.connect(_DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_inputs WHERE username = %s ORDER BY created_at DESC LIMIT %s", (username, limit))
            return cursor.fetchall()

def get_summary_after(start_date, end_date):
    username = auth.authenticate()
    with psycopg2.connect(_DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT created_at, calories, fat, protein, carbs FROM user_inputs WHERE username = %s AND created_at >= %s AND created_at <= %s ORDER BY created_at ASC", (username, start_date, end_date))
            return cursor.fetchall()

# def get_summary_all():
#     username = auth.authenticate()
#     with psycopg2.connect(_DATABASE_URL) as connection:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT created_at, calories, fat, protein, carbs FROM user_inputs WHERE username = %s ORDER BY created_at ASC", (username,))
#             return cursor.fetchall()

def get_daily_totals():
    username = auth.authenticate()
    current_date = datetime.now().date()

    # Database connection
    with psycopg2.connect(_DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            # Query for the totals of the current date for the user
            cursor.execute("SELECT id, username, calories, fat, protein, carbs, created_at FROM user_inputs WHERE username = %s AND created_at = %s", 
                           (username, current_date))
            row = cursor.fetchone()

    if row is None:
        return {
            "calories":0,
            "fat":0,
            "protein":0,
            "carbs":0,
        }
    else:
        return{
            "calories":row[2],
            "fat":row[3],
            "protein":row[4],
            "carbs":row[5]
        }

def get_user_data():
    username = auth.authenticate()
    with psycopg2.connect(_DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_data WHERE username = %s", (username,))
            table = cursor.fetchall()

    print("getting user data")
    print('table', table[0][2])
    print('table', table[0][3])
    if table:
        return {
            'calorie_goal': table[0][4],
            'fat_goal': table[0][5],
            'protein_goal': table[0][6],
            'carb_goal': table[0][7],
        }
    else:
        return  {
            'calorie_goal': -1,
            'fat_goal': -1,
            'protein_goal': -1,
            'carb_goal': -1,
        }



def insert_user_data(cal_goal, fat_goal, protein_goal, carb_goal):
    username = auth.authenticate()
    print("inserting user data")

    with psycopg2.connect(_DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            # Check if the user already exists in the user_data table
            cursor.execute("SELECT * FROM user_data WHERE username = %s", (username,))
            existing_user = cursor.fetchall()

            if existing_user:
                # Update existing record
                print('update')
                cursor.execute("UPDATE user_data SET daily_calorie_goal = %s, daily_fat_goal = %s, daily_protein_goal = %s, daily_carb_goal = %s WHERE username = %s",
                               (cal_goal, fat_goal, protein_goal, carb_goal, username))
            else:
                # Insert new record
                print('insert')
                cursor.execute("INSERT INTO user_data (username, first_name, last_name, daily_calorie_goal, daily_fat_goal, daily_protein_goal, daily_carb_goal) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                               (username,'', '', cal_goal, fat_goal, protein_goal, carb_goal))
                
            connection.commit()

# def get_description(data_7_clean, data_30_clean):
#     username = auth.authenticate()
#     current_date = datetime.now().date() 

#     with psycopg2.connect(_DATABASE_URL) as connection:
#         with connection.cursor() as cursor:
#             # Check if the user already exists in the user_data table
#             cursor.execute("SELECT * FROM descriptions WHERE username = %s AND created_at = %s", (username, current_date))
#             description = cursor.fetchall()

#             if description:
#                 return str(description[0][2])
#             else:
#                 data = {
#                     '<7day>': data_7_clean,
#                     '<30day>': data_30_clean,
#                 }
#                 qualitative_description = str(request_handler.create_qualitative_description(data))
#                 cursor.execute("INSERT INTO descriptions (username, qualitative_description, created_at) VALUES (%s, %s, %s)",
#                                (username, qualitative_description, current_date))
#                 connection.commit()
#                 return qualitative_description
                
            
