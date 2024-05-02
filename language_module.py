import request_handler

# Sends description to the API and returns the results!
def handle_description(description):
    assert len(description) > 0, 'description cannot have 0 characters'
    assert len(description) <= 5000, 'description cannot have > 5000 characters'
    values = request_handler.get_estimates(description)
    print(values)
    return values

# Testing function.
def _test(description):
    calorie_estimate, fat_estimate, protein_estimate, carb_estimate = handle_description(description)
    print("The calorie estimate is ", calorie_estimate)
    print("The fat estimate is ", fat_estimate)
    print("The protein estimate is ", protein_estimate)
    print("The carb estimate is ", carb_estimate)
    return calorie_estimate



if __name__ == '__main__':
    _test("Two reese's peanut butter cups")