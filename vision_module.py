import request_handler

# Sends user input image to the API.
# Notice the prompt chaining!
def handle_image(image):
    description = request_handler.describe_image(image)
    values = request_handler.get_estimates(description)
    print(values)
    return values


# Testing function
def _test(photo):
    calorie_estimate, fat_estimate, protein_estimate, carb_estimate = handle_image(photo)
    print("The calorie estimate is ", calorie_estimate)
    print("The fat estimate is ", fat_estimate)
    print("The protein estimate is ", protein_estimate)
    print("The carb estimate is ", carb_estimate)
    return calorie_estimate



if __name__ == '__main__':
    # Replace this with the path to an image on YOUR local computer.
    _test("/Users/jeremiahgiordani/COS333/TigerMunch_Sp2024_COS333/test_images/test_meal.jpg")