import time
from DrinkConstants import *
import thread
import ConfigParser

#import RPi.GPIO as GPIO

motor_map = MOTOR_MAP

def pour_motor(pin_num, sleep_time):
    #GPIO.output(pin_num, GPIO.LOW)
    print('pin: {}, sleep time: {}'.format(pin_num, sleep_time))
    time.sleep(sleep_time)
    #GPIO.output(pin_num, GPIO.HIGH)

class BartenderWorker():
    def __init__(self):
        self.running = False
        self.drink_map = {} # Drink name to motor number
        self.motor_map = motor_map # Motor number to pin number
        self.motor_configs = {} # [[delay1, pershot1], [delay2, pershot2]...]
    def set_board(self):
        #GPIO.setmode(GPIO.BOARD)
        for motor in self.motor_map:
            pin = self.motor_map[motor]
            #GPIO.setup(pin, GPIO.OUT)
            #GPIO.output(pin, GPIO.HIGH)
    def set_drink_map(self, new_map): # new_map is motor num to drink name
        print('Setting from drink map: {}'.format(new_map))
        self.drink_map = {}
        for motor_num in new_map:
            self.drink_map[new_map[motor_num]] = motor_num # drink name to motor num
        print('New drink map: {}'.format(self.drink_map))
    def get_motor_map(self):
        return self.motor_map
    def pour_drink(self, params):
        ing_list = params[0]
        weight = params[1]
        quan = params[2]
        print('Ingredients: {}\nWeight: {}\nQuantity: {}'.format(ing_list, weight, quan))
        alks = []
        mixes = []
        for ing in ing_list:
            if ing in ALK_MENU: alks.append(ing)
            elif ing in MIXER_MENU: mixes.append(ing)
        alk_quan = weight*quan/100.0
        mixes_quan = quan-alk_quan
        print('Alk quantity: {}'.format(alk_quan))
        print('Mixer quantity: {}'.format(mixes_quan))
        quan_per_alk = alk_quan/float(len(alks))
        quan_per_mix = mixes_quan/float(len(mixes))
        print('Quantity per alk: {}'.format(quan_per_alk))
        print('Quantity per mixer: {}'.format(quan_per_mix))
        for alk in alks:
            motor_num = self.drink_map[alk]
            pour_time = self.quan_to_time(quan_per_alk, motor_num)
            thread.start_new_thread(pour_motor, (self.motor_map[motor_num], pour_time,))
        for mix in mixes:
            motor_num = self.drink_map[mix]
            pour_time = self.quan_to_time(quan_per_mix, motor_num)
            thread.start_new_thread(pour_motor, (self.motor_map[motor_num], pour_time,))
    def pour_rail(self, params):
        for drink in params:
            motor_num = self.drink_map[drink]
            pin = self.motor_map[motor_num]
            pour_time = self.quan_to_time(params[drink], motor_num)
            thread.start_new_thread(pour_motor, (pin, pour_time,))
            
    def quan_to_time(self, quan, motor_num): # quan in shots
        if quan==0: return 0
        return self.motor_configs[motor_num]['delay']+quan*self.motor_configs[motor_num]['pershot']
    def read_config(self, addr):
        config = ConfigParser.ConfigParser()
        config.read(addr)
        for i in range(1,7):
            self.motor_configs[i] = {'delay': config.getfloat('MOTOR{}'.format(i), 'DELAY'),'pershot': config.getfloat('MOTOR{}'.format(i), 'PERSHOT')}
        
