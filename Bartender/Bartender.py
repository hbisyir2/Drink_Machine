from flask import Flask, request
import config.motors as motors
import time
from DrinkConstants import *
from thread

import RPi.GPIO as GPIO
app = Flask(__name__)

motor_map = {1: 11,
            2: 13,
            3: 15,
            4: 16,
            5: 18,
            6:22
            }

def pour_motor(pin_num, sleep_time):
    GPIO.output(pin_num, GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.output(pin_num, GPIO.HIGH)

class BartenderWorker():
    def __init__(self):
        self.running = False
        self.drink_map = {} # Drink name to motor number
        self.motor_map = motor_map # Motor number to pin number
        self.motor_configs = [
                            [2,2],
                            [2,2],
                            [2,2],
                            [2,2],
                            [2,2],
                            [2,2]] # [[delay1, pershot1], [delay2, pershot2]...]
    def set_drink_map(self, new_map): # new_map is motor num to drink name
        self.drink_map = {}
        for motor_num in new_map:
            self.drink_map[new_map[motor_num]] = motor_num # drink name to motor num
    def get_motor_map(self):
        return self.motor_map
    def pour_drink(self, ing_list, weight, quan):
        alks = []
        mixes = []
        for ing in ing_list:
            if ing in ALK_MENU: alks.append(ing)
            elif ing in MIXER_MENU: mixes.append(ing)
        alk_quan = weight*quan
        mixes_quan = quan-alk_quan ##########################
        quan_per_alk = alk_quan/float(len(alks))
        quan_per_mix = mixes_quan/float(len(mixes))
        for alk in alks:
            motor_num = self.drink_map[alk]
            pour_time = self.quan_to_time(quan_per_alk, motor_num)
            thread.start_new_thread(pour_motor, (self.motor_map[motor_num], pour_time,))
        for mix in mixes:
            motor_num = self.drink_map[mix]
            pour_time = self.quan_to_time(quan_per_mix, motor_num)
            thread.start_new_thread(pour_motor, (self.motor_map[motor_num], pour_time,))
            
    def quan_to_time(self, quan, motor_num): # quan in shots
        return self.motor_configs[motor_num][0]+quan*self.motor_configs[motor_num][1]
bartender = BartenderWorker()

@app.route('/', methods=['GET'])
def Template():
    return 'Called to root directory'

@app.route('/setup', methods=['GET'])
def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    map = bartender.get_motor_map()
    for motor_num in map:
        GPIO.setup(map[motor_num], GPIO.OUT)
        GPIO.output(map[motor_num], GPIO.HIGH)

@app.route('/cleanup', methods=['GET'])
def cleanup_gpio():
    GPIO.cleanup()

@app.route('/set_drink_map', methods=['POST'])
def set_drink_map():
    bartender.set_drink_map(request.form.get('drink_map'))

@app.route('/turn_motor_off', methods=['POST'])
def turn_off():
    bartender.turn_off(request.form.get('motors'))

@app.route('/pour_drink', methods=['POST'])
def pour_drink():
    bartender.pour_drinks(request.form.get('ing_list'), request.form.get('weight'), request.form.get('quan'))

