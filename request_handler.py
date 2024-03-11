import base64
import os
import json
import requests

def strip_json(message_content):
    content_string = message_content["choices"][0]["message"]["content"]
    json_string = content_string.strip("```\njson")
    return json.loads(json_string)



def handle_input(payload):

    if not os.environ['OPENAI_API_KEY']:
        print("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
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