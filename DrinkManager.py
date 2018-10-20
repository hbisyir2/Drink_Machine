from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App


class DrinkMaster():
    def __init__(self, config_entry_btn_cb):
        self.drinks = [] # zero based
        self.curr_drink_num = -1
        self.drink_map = {} # one based
        for i in range(1,7):
            self.drinks.append(Drink(i))
        self.config_page = ConfigPage(drink_list=self.drinks)
    def set_curr_drink(self, drink_num):
        self.curr_drink_num = drink_num
    def change_drink(self, new_drink):
        self.drinks[self.curr_drink_num-1].change_drink(new_drink)
        self.drink_map[self.curr_drink_num] = new_drink
        self.curr_drink_num = -1
    def get_drink_list(self):
        return self.drinks
    def get_config_page(self):
        return self.config_page
    def get_drink_map(self):
        return self.drink_map
    def bind_config_buttons(self, cb):
        for drink in self.drinks:
            drink.set_config_cb(cb)


# Main class for each motor
class Drink():
    def __init__(self, drink_num):
        self.drink = 'None'
        self.drink_num = drink_num
        self.config_entry = DrinkConfigEntry(drink_num=self.drink_num)
    def get_config_entry(self):
        return self.config_entry
    def change_drink(self, new_drink):
        self.config_entry.change_config_drink(new_drink)
        self.drink = new_drink
    def set_config_cb(self, cb):
        self.config_entry.set_button_cb(cb)
    def get_drink_name(self):
        return self.drink

class ConfigPage(GridLayout):
    def __init__(self, **kwargs):
        super(ConfigPage, self).__init__(cols=2,rows=3, size_hint=(1,0.8),pos_hint={"left":1, "top":1})
        drink_list = kwargs['drink_list']
        for i in range(6):
            self.add_widget(drink_list[i].get_config_entry())

# Class for each config entry, one per motor
class DrinkConfigEntry(GridLayout):
    def __init__(self, **kwargs):
        self.drink_num = kwargs['drink_num']
        super(DrinkConfigEntry, self).__init__(cols=1,rows=3)
        self.label = DrinkConfigLabel(text='None', drink_num=self.drink_num)
        self.button = DrinkConfigButton(text='Change Drink', drink_num=self.drink_num)
        self.add_widget(ConfigDrinkId(text='Drink {}'.format(self.drink_num)))
        self.add_widget(self.label)
        self.add_widget(self.button)
    def change_config_drink(self, new_drink):
        self.label.text = new_drink
    def set_button_cb(self, cb):
        self.button.bind(on_press=cb)

# Class for label on top of config entry, display drink number
class ConfigDrinkId(Label):
    def __init__(self, **kwargs):
        super(ConfigDrinkId, self).__init__(**kwargs)

# Class for label that displays drink
class DrinkConfigLabel(Label):
    def __init__(self, **kwargs):
        self.drink_num = kwargs['drink_num']
        super(DrinkConfigLabel, self).__init__(**kwargs)

# Class for button on bottom of drink config entry
class DrinkConfigButton(Button):
    def __init__(self, **kwargs):
        self.drink_num = kwargs['drink_num']
        super(DrinkConfigButton, self).__init__(**kwargs)