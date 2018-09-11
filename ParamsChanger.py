import DrinkConstants

def change_drink(motorNum, drinkName):
    if motorNum == 1:
        DrinkConstants.MOTOR_1 = drinkName
    elif motorNum == 2:
        DrinkConstants.MOTOR_2 = drinkName
    elif motorNum == 3:
        DrinkConstants.MOTOR_3 = drinkName
    elif motorNum == 4:
        DrinkConstants.MOTOR_4 = drinkName
    elif motorNum == 5:
        DrinkConstants.MOTOR_5 = drinkName
    elif motorNum == 6:
        DrinkConstants.MOTOR_6 = drinkName

def get_drink(motorNum):
    if motorNum == 1:
        return DrinkConstants.MOTOR_1
    elif motorNum == 2:
        return DrinkConstants.MOTOR_2
    elif motorNum == 3:
        return DrinkConstants.MOTOR_3
    elif motorNum == 4:
        return DrinkConstants.MOTOR_4
    elif motorNum == 5:
        return DrinkConstants.MOTOR_5
    elif motorNum == 6:
        return DrinkConstants.MOTOR_6