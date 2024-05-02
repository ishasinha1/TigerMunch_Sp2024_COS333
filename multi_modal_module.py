import request_handler

# Sends multimodal input to API and returns values!
def handle_input(image, context):
    assert len(context) > 0, 'context cannot have 0 characters'
    assert len(context) <= 5000, 'context cannot have > 5000 characters'
    description = request_handler.describe_image(image)
    values = request_handler.get_estimates(description, context)
    print(values)
    return values


# Testing function
def _test(photo, description):
    calorie_estimate, fat_estimate, protein_estimate, carb_estimate = handle_input(photo, description)
    print("The calorie estimate is ", calorie_estimate)
    print("The fat estimate is ", fat_estimate)
    print("The protein estimate is ", protein_estimate)
    print("The carb estimate is ", carb_estimate)
    return calorie_estimate



if __name__ == '__main__':
    # Replace this with the path to an image on YOUR local computer.
    _test("/Users/jeremiahgiordani/COS333/TigerMunch_Sp2024_COS333/test_images/test_meal_2.jpg", "This is a black bean quesadilla")