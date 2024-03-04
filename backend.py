from flask import Flask, render_template, request
import vision_module

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    return render_template('frontend.html')

@app.route('/get_results', methods=['GET', 'POST'])
def get_results():
    if request.method == 'POST':
        photo = request.form['photo']
        calorie_estimate, fat_estimate, protein_estimate, \
            carb_estimate = vision_module.handle_image(photo)
        return render_template('display_output.html', \
            calorie_estimate=calorie_estimate, fat_estimate=fat_estimate,\
            protein_estimate=protein_estimate, carb_estimate=carb_estimate)

if __name__ == "__main__":
    app.run()
