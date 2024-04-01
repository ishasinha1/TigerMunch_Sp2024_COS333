from flask import Flask, render_template, request, url_for, jsonify
import base64
import vision_module
import multi_modal_module
import language_module
import auth
import os
import pytz
from datetime import datetime, timedelta
import access_data
from flask import jsonify
import flask 
import urllib.parse
import time

app = Flask(__name__)

app.secret_key = os.environ['APP_SECRET_KEY']
_CAS_URL = 'https://fed.princeton.edu/cas/'

# Routes for authentication
@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()

@app.route('/logoutcas', methods=['GET'])
def logoutcas():
    return auth.logoutcas()

@app.route('/', methods=['GET', 'POST'])
def landing():
    if auth.signin() is not None:
        return flask.redirect(url_for('home')) 
    login_url = (_CAS_URL + 'login?service=' +
          urllib.parse.quote(flask.request.url))
    return render_template('landing_page.html', login_url=login_url)

@app.route('/nutrition', methods=['GET'])
def get_nutrition():
    daily_totals = access_data.get_daily_totals()
    user_data = access_data.get_user_data()
    return jsonify({
        "calories":daily_totals["calories"],
        "fat":daily_totals["fat"],
        "protein":daily_totals["protein"],
        "carbs":daily_totals["carbs"],
        "calorie_goal":user_data["calorie_goal"],
        "fat_goal":user_data["fat_goal"],
        "protein_goal":user_data["protein_goal"],
        "carb_goal":user_data["carb_goal"]
    })




@app.route('/home', methods=['GET', 'POST'])
def home():
    username = auth.authenticate()
    # Isha, you now have a variable, daily_totals, that has all of the daily totals
    # or has 0's for all of the daily totals, if the user hasn't inputted any data yet today

    return render_template('home.html', username=username)

@app.route('/upload_data', methods=['GET', 'POST'])
def form():
    username = auth.authenticate()
    return render_template('enter_meal_info.html', username=username)

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

        time.sleep(5)
        
        access_data.insert_meal(calorie_estimate, fat_estimate, protein_estimate, carb_estimate)
        username = auth.authenticate()
        return render_template('display_output.html', \
            calorie_estimate=calorie_estimate, fat_estimate=fat_estimate,\
            protein_estimate=protein_estimate, carb_estimate=carb_estimate,\
            username=username)

@app.route('/get_summary', methods=['GET', 'POST'])
def get_summary():
    table = access_data.fetch_all_data()

    meals = []
    for row in table:
        meal_dict = {
            'calories':row[2],
            'fat':row[3],
            'protein':row[4],
            'carbs':row[5],
            'created_at':row[6]
        }
        meals.append(meal_dict)
    username = auth.authenticate()
    return render_template('summary.html', meals=meals, username=username)

if __name__ == "__main__":
    app.run()

@app.route('/get_summary_values', methods=['GET'])
def get_summary_values():
    days = request.args.get('days', default=7)
    if days != 'all':
        start_date = (datetime.now() - timedelta(days=int(days))).date()
        result = access_data.get_summary_after(start_date)
    else:
        result = access_data.get_summary_all()
    data = [{'date': row[0].strftime('%Y-%m-%d'), 'calories': row[1], 'fat': row[2], 'protein': row[3], 'carbs': row[4]} for row in result]
    return jsonify(data)


@app.route('/select', methods=['GET', 'POST'])
def select():
    # username = auth.authenticate()
    if request.method == 'POST':
        account_info_dict = access_data.get_user_data()
        return jsonify(account_info_dict)
    
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    # username = auth.authenticate()
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        cal_goal = request.form['cal_goal']
        fat_goal = request.form['fat_goal']
        protein_goal = request.form['protein_goal']
        carb_goal = request.form['carb_goal']
        account_info_dict = access_data.get_user_data()
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
        
        access_data.insert_user_data(account_info_dict['first_name'], account_info_dict['last_name'], account_info_dict['calorie_goal'], account_info_dict['fat_goal'], account_info_dict['protein_goal'], account_info_dict['carb_goal'])
        #converts to a JSON response object
        return jsonify({'status': 'success'})
    
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if auth.signin() is None:
        login_url = (_CAS_URL + 'login?service=' +
          urllib.parse.quote(flask.request.url))
        return render_template('contact_us.html', username = None, login_url = login_url)            
    username = auth.authenticate()
    return render_template('contact_us.html', username = username)

@app.route('/team', methods=['GET', 'POST'])
def team():
    
    if auth.signin() is None:
        login_url = (_CAS_URL + 'login?service=' +
          urllib.parse.quote(flask.request.url))
        return render_template('team.html', username = None, login_url = login_url)     
    username = auth.authenticate()
    return render_template('team.html', username = username)