import time


class Bartender():
    def __init__(self, drinks):
        # Input drinks should be a list, with index number referring to motor number
        # Example drinks = ["coke", "rum", "", "tequila", "", "margarita mix"]
        # coke would refer to the first motor, and tequila to the fourth
        logger.debug('Bartender: __init__')
        self.drinks = drinks
        self.minimum_oz - 0.5 # An ingredient will be poured to a minimum of this level. A lower value will increase it to this mimimum

    def pour_drink(self, recipe, oz):
        # Recipe should be Recipe object type
        # oz is total oz poured for the recipe
        logger.debug('Bartender: pour_drink')
        ingredients = recipe.get_ingredients()
        # Ensure the ingredients are in the available drinks
        for ingredient in ingredients:
            if ingredient not in self.drinks:
                raise ValueError("Ingredient {} not in available drinks".format(ingredient))

        sleep_times = []
        for ingredient in ingredients:
            motor_list = [i for i, x in enumerate(self.drinks) if x == ingredient]
            p = recipe.get_percentage(ingredient)
            num_motors = len(motor_list)
            for motor_num in motor_list:
                oz_to_pour = oz*p/num_motors
                if oz_to_pour < self.minimum_oz: oz_to_pour = self.minimum_oz 
                sleep_time = self.get_motor_sleep_time(motor_num, oz_to_pour)
                self.pour_drink_motor(motor_num, sleep_time) # Start in new thread
                sleep_times.append(sleep_time)
        return max(sleep_times) # Time that the drink will take to pour

    def pour_drink_motor(self, motor, sleep_time):
        self.turn_on_motor(motor)
        time.sleep(sleep_time)
        self.turn_off_motor(motor)

    def get_motor_sleep_time(self, motor, oz):
        # return motor_delay + motor_per_oz*oz
        return 1

    def turn_on_motor(self, motor_num):
        # Change pin x from high to low
        pass

    def turn_off_motor(self, motor_num):
        # Change pin x from low to high
        pass