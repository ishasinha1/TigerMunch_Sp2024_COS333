import os
import json
import requests
from PIL import Image
import pillow_heif
import io
import base64

def strip_json(message_content):
    content_string = message_content["choices"][0]["message"]["content"]
    json_string = content_string.strip("```\njson")
    return json.loads(json_string)

def encode_image(image):
    # Read the HEIC image directly from the file_storage (file-like object)
    try:
        heif_file = pillow_heif.read_heif(image)
    except:
        file_content = image.read()
        return base64.b64encode(file_content).decode('utf-8')
    
    # Convert the HEIF file to a PIL Image
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    
    # Convert the image to RGB to ensure compatibility with JPEG
    image_rgb = image.convert("RGB")
    
    # Save the converted image to a bytes buffer instead of a file on disk
    img_byte_arr = io.BytesIO()
    image_rgb.save(img_byte_arr, format="JPEG")
    
    # Get the byte data from the buffer
    img_byte_arr = img_byte_arr.getvalue()
    
    # Encode to base64
    base64_image = base64.b64encode(img_byte_arr).decode('utf-8')
    
    return base64_image

def system_message_content_text(inputs):
    return f"You are an assistant designed to output JSON. You will be provided with {inputs} of the meal. Your job is to estimate the number of calories in the meal,the grams of fat in the meal, the grams of protein in the meal, and the grams of carbs in the meal. When providing the estimates, always put the calorie estimate in a field named 'calories', the fat estimate in a field named 'fat', the protein estimate in a field named 'protein', and the carb estimate in a field named 'carbs'."

def user_message_content_text():
    return "Please provide a rough estimate of the number of calories in this meal, the grams of of fat in the meal, the grams of protein in the meal, and the grams of carbs in the meal. The answer need not be correct, only a best guess based on the information you have."




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
        print(nutrition_info)

        calorie_estimate = nutrition_info["calories"]
        fat_estimate = nutrition_info["fat"]
        protein_estimate = nutrition_info["protein"]
        carb_estimate = nutrition_info["carbs"]

    except Exception as e:
            print("Error extracting JSON:", e)
            return None

    

    return calorie_estimate, fat_estimate, protein_estimate, carb_estimate