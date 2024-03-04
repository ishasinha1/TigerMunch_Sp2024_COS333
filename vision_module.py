from openai import OpenAI
import base64
import os
import json
import requests

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def strip_json(message_content):
    content_string = message_content["choices"][0]["message"]["content"]
    json_string = content_string.strip("```\njson")
    return json.loads(json_string)


def handle_image(image_path):

    if not os.environ['OPENAI_API_KEY']:
        print("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        return None


    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
    }

    payload = {
        "model" : "gpt-4-vision-preview",
        "messages": [
            {
            "role": "system", 
            "content": "You are an assistant designed to \
                output JSON. You will be provided with a photo of a meal. Your job \
                is to estimate the number of calories in the meal, the grams of fat \
                in the meal, the grams of protein in the meal, and the grams of carbs \
                in the meal. When providing the estimates, always put the calorie \
                estimate in a field named 'calories', the fat estimate in a field named \
                'fat', the protein estimate in a field named 'protein', and the carb \
                estimate in a field named 'carbs'. "
            },
            {
            "role": "user",
            "content": [
                {"type": "text", "text": "Please provide a rough estimate of the number \
                of calories in this meal, the grams of of fat in the meal, the \
                grams of protein in the meal, and the grams of carbs in the meal. The answer\
                need not be correct, only a best guess based on the information you have."},
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                },
                },
            ],
            }
        ],
        "max_tokens": 300
    }

    try: 
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    except Exception as e:
            print("Error in calling OpenAI API:", e)
            return None

    try:
        nutrition_info = strip_json(response.json())

        calorie_estimate = nutrition_info["calories"]
        fat_estimate = nutrition_info["fat"]
        protein_estimate = nutrition_info["protein"]
        carb_estimate = nutrition_info["carbs"]

    except Exception as e:
            print("Error extracting JSON:", e)
            return None

    

    return calorie_estimate, fat_estimate, protein_estimate, carb_estimate


def _test():
    calorie_estimate, fat_estimate, protein_estimate, carb_estimate = handle_image("/Users/jeremiah/COS333/TigerMunch_Sp2024_COS333/test_images/test_meal_4.jpg")
    print("The calorie estimate is ", calorie_estimate)
    print("The fat estimate is ", fat_estimate)
    print("The protein estimate is ", protein_estimate)
    print("The carb estimate is ", carb_estimate)



if __name__ == '__main__':
    _test()