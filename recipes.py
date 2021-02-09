


class Recipe():
    def __init__(self, name, ingredients):
        # ingredients should be dictionary with ingredient:percentage
        # Percentages must total to 1
        # Example: {"coke": 0.7, "rum": 0.3}
        logger.debug("Recipe: __init__")
        tot = 0
        for ing in ingredients:
            val = ingredients[ing]
            tot = tot+val
        if tot != 1:
            raise ValueError("Ingredient percentages must total to 1")
        self.ingredients = ingredients
        self.name = name

    def get_ingredients(self):
        return self.ingredients

    def get_percentage(self, ingredient):
        return self.ingredients[ingredient]

class Beverage():
    def __init__(self, name, alcoholic)