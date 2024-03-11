import request_handler


def handle_description(description):

    payload = {
        "model" : "gpt-4",
        "messages": [
            {
            "role": "system", 
            "content": "You are an assistant designed to \
                output JSON. You will be provided with a description of a meal. Your job \
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
                {"type": "text", "text": f"Please provide a rough estimate of the number \
                of calories in this meal, the grams of of fat in the meal, the \
                grams of protein in the meal, and the grams of carbs in the meal. The answer\
                need not be correct, only a best guess based on the information you have. Here's a description of the meal {description}"},
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