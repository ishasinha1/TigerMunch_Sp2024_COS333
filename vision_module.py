from openai import OpenAI
import base64
import os

client = OpenAI()

def handle_image(image_path):

    client = OpenAI(
        api_key=os.environ['OPENAI_API_KEY']
    )

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    response_format={"type": "json_object"},
    messages=[
        {
        {"role": "system", 
        "content": f"You are an assistant designed to \
            output JSON. You will be provided with a photo of a meal. Your job \
            is to estimate the number of calories in the meal, the grams of fat \
            in the meal, the grams of protein in the meal, and the grams of carbs \
            in the meal. When providing the estimates, always put the calorie \
            estimate in a field named 'calories', the fat estimate in a field named \
            'fat', the protein estimate in a field named 'protein', and the carb \
            estimate in a field named 'carb'. "},
        "role": "user",
        "content": [
            {"type": "text", "text": "Please provide an estimate of the number \
            of calories in this meal, the grams of of fat in the meal, the \
            grams of protein in the meal, and the grams of carbs in the meal."},
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{encoded_image}",
            },
            },
        ],
        }
    ],
    max_tokens=300,
    )

    try:
        message_content = response.choices[0].message.content
        message_json = json.loads(message_content)
        calorie_estimate = message_json["calories"]
        fat_estimate = message_json["fat"]
        protein_estimate = message_json["protein"]
        carb_estimate = message_json["carbs"]

    except Exception as e:
            print("Error in calling OpenAI API:", e)
            return

    return calorie_estimate, fat_estimate, protein_estimate, carb_estimate


