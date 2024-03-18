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

def get_user_data(first_name, last_name, cal_goal, fat_goal, protein_goal, carb_goal):
    username = auth.authenticate()
    with psycopg2.connect(_DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_data WHERE username = %s", (username,))
            table = cursor.fetchall()


    if table:
        account_info_dict = {
            'first_name': table[0][2],
            'last_name': table[0][3],
            'calorie_goal': table[0][4],
            'fat_goal': table[0][5],
            'protein_goal': table[0][6],
            'carb_goal': table[0][7],
        }
    else:
        account_info_dict = {
            'first_name': '',
            'last_name': '',
            'calorie_goal': -1,
            'fat_goal': -1,
            'protein_goal': -1,
            'carb_goal': -1,
        }

    print(cal_goal)
    if first_name is not None:
        account_info_dict['first_name'] = first_name
    if last_name is not None:
        account_info_dict['last_name'] = last_name

    if cal_goal is not None:
        print("changed CALORIES!!")
        if cal_goal == '':
            account_info_dict['calorie_goal'] = -1
        else:
            account_info_dict['calorie_goal'] = cal_goal
    if fat_goal is not None:
        if fat_goal == '':
            account_info_dict['fat_goal'] = -1
        else:
            account_info_dict['fat_goal'] = fat_goal

    if protein_goal is not None:
        if protein_goal == '':
            account_info_dict['protein_goal'] = -1
        else:
            account_info_dict['protein_goal'] = protein_goal 

    if carb_goal is not None:
        if carb_goal == '':
            account_info_dict['carb_goal'] = -1
        else:
            account_info_dict['carb_goal'] = carb_goal 
    
    insert_user_data(account_info_dict['first_name'], account_info_dict['last_name'], account_info_dict['calorie_goal'], account_info_dict['fat_goal'], account_info_dict['protein_goal'], account_info_dict['carb_goal'])

    return account_info_dict

def insert_user_data(first_name, last_name, cal_goal, fat_goal, protein_goal, carb_goal):
    username = auth.authenticate()

    with psycopg2.connect(_DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            # Check if the user already exists in the user_data table
            cursor.execute("SELECT * FROM user_data WHERE username = %s", (username,))
            existing_user = cursor.fetchall()

            if existing_user:
                # Update existing record
                cursor.execute("UPDATE user_data SET first_name = %s, last_name = %s, daily_calorie_goal = %s, daily_fat_goal = %s, daily_protein_goal = %s, daily_carb_goal = %s WHERE username = %s",
                               (first_name, last_name, cal_goal, fat_goal, protein_goal, carb_goal, username))
            else:
                # Insert new record
                cursor.execute("INSERT INTO user_data (username, first_name, last_name, daily_calorie_goal, daily_fat_goal, daily_protein_goal, daily_carb_goal) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                               (username, first_name, last_name, cal_goal, fat_goal, protein_goal, carb_goal))
                
            connection.commit()
