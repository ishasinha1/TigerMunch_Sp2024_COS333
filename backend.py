from flask import Flask, render_template, request
import base64
import vision_module
import multi_modal_module
import language_module
import auth
import os
import psycopg2
import pytz
from datetime import datetime


app = Flask(__name__)

app.secret_key = os.environ['APP_SECRET_KEY']

_DATABASE_URL = os.environ['DATABASE_URL']

# Routes for authentication.

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()

@app.route('/logoutcas', methods=['GET'])
def logoutcas():
    return auth.logoutcas()

@app.route('/', methods=['GET', 'POST'])
def home():
    username = auth.authenticate()
    return render_template('home.html', username=username)

@app.route('/upload_data', methods=['GET', 'POST'])
def form():
    return render_template('enter_meal_info.html')

@app.route('/get_results', methods=['GET', 'POST'])
def get_results():
    if request.method == 'POST':
        photo = request.files.get('photo')
        description = request.form.get('description')

        if photo and description:
            print("running multi-modal")
            calorie_estimate, fat_estimate, protein_estimate, \
            carb_estimate = multi_modal_module.handle_input(photo, description)
        elif photo:
            print("running image module")
            calorie_estimate, fat_estimate, protein_estimate, \
            carb_estimate = vision_module.handle_image(photo)
        elif description:
            print("running language module")
            calorie_estimate, fat_estimate, protein_estimate, \
            carb_estimate = language_module.handle_description(description)
        else:
            return 'No input provided', 400

        username = auth.authenticate()

        with psycopg2.connect(_DATABASE_URL) as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO user_inputs (username, calories, fat, protein, carbs) VALUES (%s, %s, %s, %s, %s)", (username, calorie_estimate, fat_estimate, protein_estimate, carb_estimate))
                connection.commit()
            
        return render_template('display_output.html', \
            calorie_estimate=calorie_estimate, fat_estimate=fat_estimate,\
            protein_estimate=protein_estimate, carb_estimate=carb_estimate)

@app.route('/get_summary', methods=['GET', 'POST'])
def get_summary():
    username = auth.authenticate()
    with psycopg2.connect(_DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_inputs WHERE username = %s ORDER BY created_at ASC", (username,))
            table = cursor.fetchall()

    est = pytz.timezone('US/Eastern')
    meals = []
    for row in table:
        est_time = row[6].astimezone(est)
        meal_dict = {
            'calories':row[2],
            'fat':row[3],
            'protein':row[4],
            'carbs':row[5],
            'created_at':est_time.strftime('%Y-%m-%d %I:%M %p')
        }
        meals.append(meal_dict)

    return render_template('summary.html', meals=meals)

if __name__ == "__main__":
    app.run()
