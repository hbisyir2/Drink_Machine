import time
import datetime
from kivy.lang import Builder
from DrinkConstants import *
import ParamsChanger as pc
from DrinkManager import *
from DrinkMaker import *
from Bartender import BartenderWorker
import requests
import emoji
import ConfigParser

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader

BARTENDER_ADDR = "127.0.0.1"
BARTENDER_PORT = 5000

CONFIG_ADDR = 'motor_timing.ini'








def ConfigCB(instance):
    dm.set_curr_drink(instance.drink_num)
    App.get_running_app().root.current = "configmotor"

def change_time_btn_cb(instance):
    #Window.clearcolor = (54/255.0, 192/255.0, 194/255.0, 1)
    dm.set_curr_drink(instance.drink_num)
    App.get_running_app().root.current = "timing"

def changedrink(instance):
    dm.change_drink(instance.text)
    App.get_running_app().root.current = "config"

def changerail(instance):
    menu.change_rail(instance.text)

def gohome(instance): # Call back for button button on config menu
    bar.set_drink_map(dm.get_drink_map())
    bar.read_config(CONFIG_ADDR)
    menu.generate_drink_list(dm.get_drink_list())
    App.get_running_app().root.current = "home"

def return_to_configure(instance):
    App.get_running_app().root.current = "config"

def pour_drink(instance):
    params = menu.get_pour_params(instance.recipe_name)
    bar.pour_drink(params)
   
    
def rail_select(instance):
    menu.change_rail_drink(instance.text)
    App.get_running_app().root.current = "home"
    
def change_rail(instance):
    menu.set_active_rail(instance.text)
    drinks = dm.get_drink_names()
    menu.reload_rail_list(drinks, rail_select)
    App.get_running_app().root.current = "configrail"

def simple_go_home(instance):
    App.get_running_app().root.current = "home"
    
def pour_rail(instance):
    params = menu.get_rail_pour_params()
    print(params)
    bar.pour_rail(params)
    
    
    
    
    
    
    

dm = DrinkMaster(ConfigCB)
menu = Menu()
menu.bind_pour_buttons(pour_drink)
menu.bind_rail_buttons(change_rail, pour_rail)
bar = BartenderWorker()
bar.set_board()

class RailSelectScreen(GridLayout):
    def __init__(self, **kwargs):
        super(RailSelectScreen, self).__init__(cols=2)
        for drink in DRINKS_MENU:
            self.add_widget(DrinkSelectButton(text=drink, on_press=rail_select))

class DrinkSelectScreen(GridLayout):
    def __init__(self, **kwargs):
        super(DrinkSelectScreen, self).__init__(cols=2)
        for drink in DRINKS_MENU:
            self.add_widget(DrinkSelectButton(text=drink, on_press=changedrink))

class DrinkSelectButton(Button):
    def __init__(self, **kwargs):
        if kwargs['text'] in ALK_MENU: kwargs['background_color'] = [1,0,0,.75]
        else: kwargs['background_color'] = [0,1,0,.75]
        super(DrinkSelectButton, self).__init__(**kwargs)
    

class ScreenManagement(ScreenManager):
    pass

class ConfigScreen(Screen):
    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(name='config')
        layout = FloatLayout()
        dm.bind_config_buttons(ConfigCB, change_time_btn_cb)
        layout.add_widget(dm.get_config_page())
        layout.add_widget(Button(
                                #text=emoji.emojize('Start Drinking :thumbs_up'),
                                text='Start Drinking XD',
                                font_size=44,
                                size_hint=(1,0.2),
                                pos_hint={"left":1, "bottom":1},
                                on_press = gohome,
                                ))
        self.add_widget(layout)

class HomePage(Screen):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(name='home')
        #layout = FloatLayout()
        HomePanelBoard = TabbedPanel(do_default_tab = False)
        CocktailPanel = TabbedPanelHeader(text='Cocktails')
        CocktailPanel.content = menu.get_drink_menu()
        
        RailPanel = TabbedPanelHeader(text='Rails')
        RailPanel.content = menu.get_rail_menu()
        
        HomePanelBoard.add_widget(CocktailPanel)
        HomePanelBoard.add_widget(RailPanel)
        
        # layout.add_widget(Button(
                                # text='Return to Configuration',
                                # size_hint=(1,0.2),
                                # pos_hint={"left":1, "bottom":1},
                                # on_press = return_to_configure))
        self.add_widget(HomePanelBoard)
        

class TimingPage(Screen):
    def __init__(self, **kwargs):
        self.start = 0
    
        super(TimingPage, self).__init__(name='timing')
        self.layout = FloatLayout()
        self.label = TimingInstructions(
            text='INSTRUCTIONS:\n'+
                'This is a page to determine the timing of pouring one shot.\n'+
                'Press the button below and the drink will start to pour,\n'+
                'Press the button again when the drink STARTS TO POUR and the liquid starts entering the cup,\n'+
                'Press the button again after ONE SHOT HAS BEEN POURED',
            size_hint=(1,0.5),
            pos_hint={"left":1, "top":1},
            )
        self.button = Button(
            text='START POURING',
            on_press=self.start_pour,
            size_hint=(1,0.5),
            pos_hint={"left":1, "bottom":1},)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)
                                
        self.add_widget(self.layout)
    def start_pour(self, instance):
        self.start = datetime.datetime.now()
        self.layout.remove_widget(self.button)
        self.button = Button(
            text='PRESS WHEN LIQUID STARTS POURING',
            on_press=self.flow_started,
            size_hint=(1,0.5),
            pos_hint={"left":1, "bottom":1},)
        self.layout.add_widget(self.button)

    def flow_started(self, instance):
        self.t1 = datetime.datetime.now()
        self.layout.remove_widget(self.button)
        self.button = Button(
            text='PRESS WHEN ONE SHOT HAS BEEN POURED',
            on_press=self.stop_flow,
            size_hint=(1,0.5),
            pos_hint={"left":1, "bottom":1},)
        self.layout.add_widget(self.button)
    def stop_flow(self, instance):
        self.t2 = datetime.datetime.now()
        self.layout.remove_widget(self.button)
        self.button = Button(
            text='ACCEPT',
            on_press=self.accept_timing,
            size_hint=(1,0.5),
            pos_hint={"left":1, "bottom":1},)
        self.layout.add_widget(self.button)
        delay = self.t1-self.start
        self.delay=delay.total_seconds()
        pershot=self.t2-self.t1
        self.pershot=pershot.total_seconds()
        self.label.text = 'FINISHED:\nDelay: {} second\nTime per Shot: {} second'.format(delay, pershot)
    def accept_timing(self, instance):
        App.get_running_app().root.current = "config"
        config = ConfigParser.ConfigParser()
        config.read(CONFIG_ADDR)
        config.set('MOTOR{}'.format(dm.get_curr_drink()),'DELAY',self.delay)
        config.set('MOTOR{}'.format(dm.get_curr_drink()),'PERSHOT',self.pershot)
        with open(CONFIG_ADDR, 'w') as configfile:
            config.write(configfile)
        dm.set_curr_drink(-1)
        self.reset_page()
    def reset_page(self):
        self.clear_widgets()
        self.layout = FloatLayout()
        self.label = TimingInstructions(
            text='INSTRUCTIONS:\n'+
                'This is a page to determine the timing of pouring one shot.\n'+
                'Press the button below and the drink will start to pour,\n'+
                'Press the button again when the drink STARTS TO POUR and the liquid starts entering the cup,\n'+
                'Press the button again after ONE SHOT HAS BEEN POURED',
            size_hint=(1,0.5),
            pos_hint={"left":1, "top":1},
            )
        self.button = Button(
            text='START POURING',
            on_press=self.start_pour,
            size_hint=(1,0.5),
            pos_hint={"left":1, "bottom":1},)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)
                                
        self.add_widget(self.layout)
        
class TimingInstructions(Label):
    def __init__(self, **kwargs):
        super(TimingInstructions, self).__init__(**kwargs)              

class ConfigMotor(Screen):
    pass

class MyLabel(Label):
    pass

class ConfigRail(Screen):
    def __init__(self, **kwargs):
        super(ConfigRail, self).__init__(name='configrail')
        layout = FloatLayout()
        layout.add_widget(menu.get_rail_drink_menu())
        layout.add_widget(Button(
            size_hint=(1,0.2),
            pos_hint={"left":1, "bottom":1},
            text="Go Back",
            on_press=simple_go_home,
            fone_size=40,
            background_color = [.247,.498,.749,1]
        ))
        self.add_widget(layout)
            
presentation = Builder.load_file("DrinkMachineMain.kv")
class DrinkMachineGUI(App):
    def build(self):
        return presentation

if __name__ == '__main__':
    DrinkMachineGUI().run()

