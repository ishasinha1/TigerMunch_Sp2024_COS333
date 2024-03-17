import request_handler


def handle_description(description):
    user_message_content = request_handler.user_message_content_text() + f" Here's a description of the meal {description}"
    payload = {
        "model" : "gpt-4",
        "seed": 1,
        "messages": [
            {
            "role": "system", 
            "content": request_handler.system_message_content_text("a written description")
            },
            {
            "role": "user",
            "content": [
                {"type": "text", "text": user_message_content},
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


def _test(description):
    calorie_estimate, fat_estimate, protein_estimate, carb_estimate = handle_description(description)
    print("The calorie estimate is ", calorie_estimate)
    print("The fat estimate is ", fat_estimate)
    print("The protein estimate is ", protein_estimate)
    print("The carb estimate is ", carb_estimate)
    return calorie_estimate



if __name__ == '__main__':
    _test("Two reese's peanut butter cups")