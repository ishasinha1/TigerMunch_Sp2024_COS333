import request_handler


def handle_image(image):
    base64_image = request_handler.encode_image(image)

    payload = {
        "model" : "gpt-4-vision-preview",
        "messages": [
            {
            "role": "system", 
            "content": request_handler.system_message_content_text("a photograph")
            },
            {
            "role": "user",
            "content": [
                {"type": "text", "text": request_handler.user_message_content_text()},
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


def _test(photo):
    calorie_estimate, fat_estimate, protein_estimate, carb_estimate = handle_image(photo)
    print("The calorie estimate is ", calorie_estimate)
    print("The fat estimate is ", fat_estimate)
    print("The protein estimate is ", protein_estimate)
    print("The carb estimate is ", carb_estimate)
    return calorie_estimate



if __name__ == '__main__':
    _test("/Users/jeremiahgiordani/COS333/TigerMunch_Sp2024_COS333/test_images/test_meal.jpg")