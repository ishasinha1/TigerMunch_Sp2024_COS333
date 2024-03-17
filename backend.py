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

        
        access_data.insert_meal(calorie_estimate, fat_estimate, protein_estimate, carb_estimate)
            
        return render_template('display_output.html', \
            calorie_estimate=calorie_estimate, fat_estimate=fat_estimate,\
            protein_estimate=protein_estimate, carb_estimate=carb_estimate)

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

    return render_template('summary.html', meals=meals)

if __name__ == "__main__":
    app.run()

@app.route('/account', methods=['GET', 'POST'])
def get_account():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    cal_goal = request.args.get('cal_goal')
    fat_goal = request.args.get('fat_goal')
    protein_goal = request.args.get('protein_goal')
    carb_goal = request.args.get('carb_goal')

    # if any of the goals are not an integer value or 'None' or None, we must send the user an error message and let them know that the values must be integers

    account_info_dict = access_data.get_user_data(first_name, last_name, cal_goal, fat_goal, protein_goal, carb_goal)

    return render_template('account.html', account_info_dict=account_info_dict)

