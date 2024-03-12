from flask import Flask, render_template, request
import base64
import vision_module
import multi_modal_module
import language_module


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
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
            
        return render_template('display_output.html', \
            calorie_estimate=calorie_estimate, fat_estimate=fat_estimate,\
            protein_estimate=protein_estimate, carb_estimate=carb_estimate)



if __name__ == "__main__":
    app.run()
