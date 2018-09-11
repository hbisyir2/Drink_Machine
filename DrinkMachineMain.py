import time
from kivy.lang import Builder
import DrinkConstants as dc
import ParamsChanger as pc

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

#global DrinkLabel_1 = Label(text='None')

def ConfigCB(instance):
    dc.CURRENT_MOTOR = instance.motorNum
    App.get_running_app().root.current = "configmotor"

def ChangeDrinkCB(instance):
    print('Changing motor {} to {}'.format(dc.CURRENT_MOTOR, instance.text))
    if dc.CURRENT_MOTOR == 1:
        dc.DrinkLabel_1.text = instance.text
        print(True)
    elif dc.CURRENT_MOTOR == 2:
        dc.DrinkLabel_2.text = instance.text
    elif dc.CURRENT_MOTOR == 3:
        dc.DrinkLabel_3.text = instance.text
    elif dc.CURRENT_MOTOR == 4:
        dc.DrinkLabel_4.text = instance.text
    elif dc.CURRENT_MOTOR == 5:
        dc.DrinkLabel_5.text = instance.text
    elif dc.CURRENT_MOTOR == 6:
        dc.DrinkLabel_6.text = instance.text
    dc.DrinkLabel_6.text = instance.text
    App.get_running_app().root.current = "config"

class ScreenManagement(ScreenManager):
    pass

class ConfigScreen(Screen):
    pass

class HomePage(Screen):
    pass

class ConfigMotor(Screen):
    pass

class MyLabel(Label):
    pass

class DrinkSelectScreen(GridLayout):
    def __init__(self, **kwargs):
        super(DrinkSelectScreen, self).__init__(cols=2)
        for drink in dc.DRINKS_MENU:
            self.add_widget(DrinkSelectButton(text=drink, on_press=ChangeDrinkCB))
    
class DrinkSelectButton(Button):
    def __init__(self, **kwargs):
        super(DrinkSelectButton, self).__init__(**kwargs)

class MotorConfigButton(Button):
    def __init__(self, motorNum, **kwargs):
        self.motorNum = motorNum
        super(MotorConfigButton, self).__init__(**kwargs)

class ConfigEntry(GridLayout):
    def __init__(self, drink_num):
        super(ConfigEntry, self).__init__(cols=1,rows=3)
        self.motorNum = drink_num
        self.drink_label = Label(text='None')
        self.add_widget(Label(text='Drink {}'.format(self.motorNum)))
        if drink_num == 1:
            self.add_widget(dc.DrinkLabel_1)
        elif drink_num == 2:
            self.add_widget(dc.DrinkLabel_2)
        elif drink_num == 3:
            self.add_widget(dc.DrinkLabel_3)
        elif drink_num == 4:
            self.add_widget(dc.DrinkLabel_4)
        elif drink_num == 5:
            self.add_widget(dc.DrinkLabel_5)
        elif drink_num == 6:
            self.add_widget(dc.DrinkLabel_6)
        self.add_widget(MotorConfigButton(self.motorNum, text="Change Drink", on_press=ConfigCB))
    def change_drink(self, instance):
        self.drink_label.text = instance.text
        

class ConfigPage(GridLayout):
    def __init__(self, **kwargs):
        super(ConfigPage, self).__init__(cols=2,rows=3)
        for i in range(6):
            self.add_widget(ConfigEntry(i+1))
    
presentation = Builder.load_file("DrinkMachineMain.kv")
class DrinkMachineGUI(App):
    def build(self):
        return presentation

if __name__ == '__main__':
    DrinkMachineGUI().run()

