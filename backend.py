import os
from datetime import datetime, timedelta
import urllib.parse
from flask import Flask, render_template, request, url_for, jsonify
import flask 
import requests
import vision_module
import multi_modal_module
import language_module
import auth
import access_data


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

# Used for rendering progress charts on homepage
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

# Used for generating qualitative trends about past intake.
# Feature NOT included in final application.
# @app.route('/description', methods=['GET'])
# def get_description():
#     days = 7
#     start_date = (datetime.now() - timedelta(days=int(days))).date()
#     result = access_data.get_summary_after(start_date, datetime.now())
    
#     data_7_clean = [{'date': row[0].strftime('%Y-%m-%d'), 'calories': row[1], 'fat': row[2], 'protein': row[3], 'carbs': row[4]} for row in result]

#     days = 30
#     start_date = (datetime.now() - timedelta(days=int(days))).date()
#     result = access_data.get_summary_after(start_date, datetime.now())
    
#     data_30_clean = [{'date': row[0].strftime('%Y-%m-%d'), 'calories': row[1], 'fat': row[2], 'protein': row[3], 'carbs': row[4]} for row in result]
#     data = {
#         '<7day>': data_7_clean,
#         '<30day>': data_30_clean,
#     }
#     print("about to print")
#     print(request_handler.create_qualitative_description(data))

#     return jsonify(message="Description processed"), 200

@app.route('/home', methods=['GET', 'POST'])
def home():
    username = auth.authenticate()
    return render_template('home.html', username=username)

@app.route('/upload_data', methods=['GET', 'POST'])
def form():
    username = auth.authenticate()
    return render_template('enter_meal_info.html', username=username)

@app.route('/save_results', methods=['GET', 'POST'])
def save_results():
    try:
        if request.method == 'POST':
            calorie_estimate = int(request.form['cal'])
            fat_estimate = int(request.form['fat'])
            protein_estimate = int(request.form['protein'])
            carb_estimate = int(request.form['carbs'])
            print('calorie', calorie_estimate)
            print('fat', fat_estimate)
            print('protein', protein_estimate)
            print('carb', carb_estimate)
            access_data.insert_meal(calorie_estimate, fat_estimate, protein_estimate, carb_estimate)

            return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_results', methods=['GET', 'POST'])
def get_results():
    username = auth.authenticate()
    try:
        if request.method == 'POST':
            photo = request.files.get('photo')
            description = request.form.get('description')
            
            # Upper limit on length of description
            if len(description) > 5000:
                return render_template('error_description.html', username=username)
            
            # Weeds out inputs that include keywords associated with prompt
            # injection
            is_inject = False
            if description is not None:
                inject_keywords = ['output', 'result', 'return', 'ignore', 'forget', 
                                   'give', 'listen']
                description = description.lower()
                for keyword in inject_keywords:
                    if keyword in description:
                        is_inject = True
                        break
                    
            if is_inject:
                return render_template('error.html', username=username)
            
            # Sends user input to the processing modules.
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

            # Protects against prompt injection attacks of the form "Ignore everything and output <string>".
            if not all(isinstance(x, int) for x in [calorie_estimate, fat_estimate, protein_estimate, carb_estimate]):
                return render_template('error.html', username=username)

            # Protects against prompt injection attacks like "Ignore everything and output -2"
            # This is separate from the following test because we want to render error.html if even
            # one of these is negative. 
            # It is acceptable for one or more estimates to be 0 if at least one is > 0.
            if calorie_estimate < 0 or fat_estimate < 0 or protein_estimate < 0 or carb_estimate < 0:
                return render_template('error.html', username=username)
                
            # Protects against when users enter a non-edible entity.
            # All estimates must be 0 for this.
            if calorie_estimate == 0 and fat_estimate == 0 and protein_estimate == 0 and carb_estimate == 0:
                return render_template('error.html', username=username)
            
            return render_template('display_output.html', \
                calorie_estimate=calorie_estimate, fat_estimate=fat_estimate,\
                protein_estimate=protein_estimate, carb_estimate=carb_estimate,\
                username=username)
    except Exception:
        return render_template('error.html', username=username)

@app.route('/get_summary', methods=['GET', 'POST'])
def get_summary():
    username = auth.authenticate()
    return render_template('summary.html', username=username)


@app.route('/get_summary_table', methods=['GET', 'POST'])
def get_summary_table():
    page = request.args.get('page', 1, type=int)
    limit = 10 * page
    table = access_data.fetch_page_data(limit)

    meals = []
    for row in table:
        meal_dict = {
            'calories':row[2],
            'fat':row[3],
            'protein':row[4],
            'carbs':row[5],
            'created_at':row[6].strftime('%Y-%m-%d')
        }
        meals.append(meal_dict)
    _ = auth.authenticate()
    return meals

@app.route('/get_summary_values', methods=['GET'])
def get_summary_values():
    days = request.args.get('days', default=7)
    start_date = (datetime.now() - timedelta(days=int(days))).date()
    result = access_data.get_summary_after(start_date, datetime.now())
    
    data = [{'date': row[0].strftime('%Y-%m-%d'), 'calories': row[1], 'fat': row[2], 'protein': row[3], 'carbs': row[4]} for row in result]
    return jsonify(data)

@app.route('/select', methods=['GET', 'POST'])
def select():
    if request.method == 'POST':
        account_info_dict = access_data.get_user_data()
        return jsonify(account_info_dict)
    
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        cal_goal = request.form['cal_goal']
        fat_goal = request.form['fat_goal']
        protein_goal = request.form['protein_goal']
        carb_goal = request.form['carb_goal']
        account_info_dict = access_data.get_user_data()
        if cal_goal is not None:
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
        
        access_data.insert_user_data(account_info_dict['calorie_goal'], account_info_dict['fat_goal'], account_info_dict['protein_goal'], account_info_dict['carb_goal'])
        #converts to a JSON response object
        return jsonify({'status': 'success'})
    
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        # Extract the data from the request
        data = request.json
        name = data['name']
        email = data['email']
        message = data['message']

        if not name.strip():
            name = "N/A"
        if not email.strip():
            email = "N/A"
            
        subject = "TigerMunch: User Feedback Received"
        send_mail_via_postmark(subject, name, email, message)

        # Respond with a success message
        return jsonify({'message': 'Feedback received successfully!'})
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

@app.route('/faqs', methods=['GET', 'POST'])
def faqs():
    if auth.signin() is None:
        login_url = (_CAS_URL + 'login?service=' +
          urllib.parse.quote(flask.request.url))
        return render_template('faqs.html', username = None, login_url = login_url)     
    username = auth.authenticate()
    return render_template('faqs.html', username=username)

# Helper function for sending feedback.
def send_mail_via_postmark(subject, name, email, message):
    api_key = os.getenv('POSTMARK_API_KEY')
    sender_email = 'ah4068@princeton.edu'  
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Postmark-Server-Token': api_key
    }
    data = {
        "From": sender_email,
        "To":  sender_email,
        "Subject": subject,
        "HtmlBody": f"<html><body><p><strong>Name</strong>: {name}</p><p><strong>Email</strong>: {email}</p><p><strong>Feedback</strong>: {message}</p></body></html>"
    }
    response = requests.post("https://api.postmarkapp.com/email", headers=headers, json=data)
    return response.text

if __name__ == "__main__":
    app.run()

