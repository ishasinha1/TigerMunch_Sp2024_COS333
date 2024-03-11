from flask import Flask, render_template, request
import base64
import vision_module


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    return render_template('frontend.html')

@app.route('/get_results', methods=['GET', 'POST'])
def get_results():
    if request.method == 'POST':
        if 'photo' not in request.files:
            return 'No file part', 400
        photo = request.files['photo']
        if photo.filename == '':
            return 'No selected file', 400
        calorie_estimate, fat_estimate, protein_estimate, \
            carb_estimate = vision_module.handle_image(photo)
        return render_template('display_output.html', \
            calorie_estimate=calorie_estimate, fat_estimate=fat_estimate,\
            protein_estimate=protein_estimate, carb_estimate=carb_estimate)

def convert_image_to_base64(file):
    file_content = file.read()
    return base64.b64encode(file_content).decode('utf-8')



if __name__ == "__main__":
    app.run()
