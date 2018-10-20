import time
from kivy.lang import Builder
import DrinkConstants as dc
import ParamsChanger as pc
from DrinkManager import *
from DrinkMaker import *
import requests

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.slider import Slider

BARTENDER_ADDR = "127.0.0.1"
BARTENDER_PORT = 5000

def ConfigCB(instance):
    dm.set_curr_drink(instance.drink_num)
    App.get_running_app().root.current = "configmotor"

def changedrink(instance):
    dm.change_drink(instance.text)
    App.get_running_app().root.current = "config"

def gohome(instance): # Call back for button button on config menu
    requests.post('http://{}/set_drink_map:{}/'.format(BARTENDER_ADDR, BARTENDER_PORT), data={'drink_map': dm.get_drink_list()})
    App.get_running_app().root.current = "home"

def return_to_configure(instance):
    App.get_running_app().root.current = "config"

def pour_drink(instance):
    params = menu.get_pour_params(instance.recipe_name)
    requests.post('http://{}/pour_drink:{}/'.format(BARTENDER_ADDR, BARTENDER_PORT), data={'ing_list': params[0], 'weight': params[1], 'quan': params[2]})

dm = DrinkMaster(ConfigCB)
menu = Menu()
menu.bind_pour_buttons(pour_drink)

class DrinkSelectScreen(GridLayout):
    def __init__(self, **kwargs):
        super(DrinkSelectScreen, self).__init__(cols=2)
        for drink in dc.DRINKS_MENU:
            self.add_widget(DrinkSelectButton(text=drink, on_press=changedrink))

class DrinkSelectButton(Button):
    def __init__(self, **kwargs):
        super(DrinkSelectButton, self).__init__(**kwargs)

class ScreenManagement(ScreenManager):
    pass

class ConfigScreen(Screen):
    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(name='config')
        layout = FloatLayout()
        dm.bind_config_buttons(ConfigCB)
        layout.add_widget(dm.get_config_page())
        layout.add_widget(Button(
                                text='Start Drinking',
                                size_hint=(1,0.2),
                                pos_hint={"left":1, "bottom":1},
                                on_press = gohome))
        self.add_widget(layout)

class HomePage(Screen):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(name='home')
        layout = FloatLayout()
        layout.add_widget(menu.get_drink_menu())
        layout.add_widget(Button(
                                text='Return to Configuration',
                                size_hint=(1,0.2),
                                pos_hint={"left":1, "bottom":1},
                                on_press = return_to_configure))
        self.add_widget(layout)

class ConfigMotor(Screen):
    pass

class MyLabel(Label):
    pass


    
presentation = Builder.load_file("DrinkMachineMain.kv")
class DrinkMachineGUI(App):
    def build(self):
        return presentation

if __name__ == '__main__':
    DrinkMachineGUI().run()

