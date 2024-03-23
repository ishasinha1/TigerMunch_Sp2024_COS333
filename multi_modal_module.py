import request_handler


# def encode_image_path(image_path):
#   with open(image_path, "rb") as image_file:
#     return base64.b64encode(image_file.read()).decode('utf-8')



def handle_input(image, context):
    description = request_handler.describe_image(image)
    values = request_handler.get_estimates(description, context)
    print(values)
    return values



def _test(photo, description):
    calorie_estimate, fat_estimate, protein_estimate, carb_estimate = handle_input(photo, description)
    print("The calorie estimate is ", calorie_estimate)
    print("The fat estimate is ", fat_estimate)
    print("The protein estimate is ", protein_estimate)
    print("The carb estimate is ", carb_estimate)
    return calorie_estimate



if __name__ == '__main__':
    _test("/Users/jeremiahgiordani/COS333/TigerMunch_Sp2024_COS333/test_images/test_meal_2.jpg", "This is a black bean quesadilla")