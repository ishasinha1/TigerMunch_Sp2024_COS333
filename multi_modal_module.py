import request_handler


# def encode_image_path(image_path):
#   with open(image_path, "rb") as image_file:
#     return base64.b64encode(image_file.read()).decode('utf-8')



def handle_input(image, description):


    base64_image = request_handler.encode_image(image)
    user_message_content = request_handler.user_message_content_text() + f" Here's a description of the meal {description}"

    payload = {
        "model" : "gpt-4-vision-preview",
        "messages": [
            {
            "role": "system", 
            "content": request_handler.system_message_content_text()
            },
            {
            "role": "user",
            "content": [
                {"type": "text", "text": user_message_content},
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
        return request_handler.handle_input(payload)

    except Exception as e:
        print("Error in calling OpenAI API:", e)
        return None


def _test(photo, description):
    calorie_estimate, fat_estimate, protein_estimate, carb_estimate = handle_input(photo, description)
    print("The calorie estimate is ", calorie_estimate)
    print("The fat estimate is ", fat_estimate)
    print("The protein estimate is ", protein_estimate)
    print("The carb estimate is ", carb_estimate)
    return calorie_estimate



if __name__ == '__main__':
    _test("/Users/jeremiahgiordani/COS333/TigerMunch_Sp2024_COS333/test_images/test_meal_2.jpg", "This is a black bean quesadilla")