from flask import Flask, render_template, request
import base64
import vision_module
import multi_modal_module
import language_module
import auth
import os
import pytz
from datetime import datetime
import access_data
from flask import jsonify

app = Flask(__name__)

app.secret_key = os.environ['APP_SECRET_KEY']

# Routes for authentication.

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()

@app.route('/logoutcas', methods=['GET'])
def logoutcas():
    return auth.logoutcas()

@app.route('/', methods=['GET', 'POST'])
# def landing():
#     username = auth.authenticate()
#     return render_template('landing_page.html', username=username)

# @app.route('/home', methods=['GET', 'POST'])
def home():
    username = auth.authenticate()
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

        
        access_data.insert_meal(calorie_estimate, fat_estimate, protein_estimate, carb_estimate)
        username = auth.authenticate()
        return render_template('display_output.html', \
            calorie_estimate=calorie_estimate, fat_estimate=fat_estimate,\
            protein_estimate=protein_estimate, carb_estimate=carb_estimate, username=username)

@app.route('/get_summary', methods=['GET', 'POST'])
def get_summary():
    table = access_data.fetch_all_data()

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
    username = auth.authenticate()
    return render_template('summary.html', meals=meals, username=username)

if __name__ == "__main__":
    app.run()

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
    username = auth.authenticate()
    return render_template('contact_us.html', username = username)

@app.route('/team', methods=['GET', 'POST'])
def team():
    username = auth.authenticate()
    return render_template('team.html', username = username)