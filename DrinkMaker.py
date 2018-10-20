from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.app import App

class Menu:
    def __init__(self):
        self.drinks = [RumCoke(), TequilaSunrise(), WhiskeyGinger(), Margarita()]
        self.drink_menu = DrinkMakeMenu()
        self.pour_cb = None
    def generate_drink_list(self, raw_drinks):
        mixers = []
        self.available = []
        for drink in raw_drinks:
            mixers.append(drink.get_drink_name())
            print('Adding mixer: {}'.format(drink.get_drink_name()))
        for drink in self.drinks:
            if self.is_available(mixers, drink):
                self.available.append(drink)
                
        print('Available: {}'.format(self.available))
        self.drink_menu.reload_menu(self.available)
        self.drink_menu.bind_pour_btn(self.pour_cb)
        return self.available
            
    def is_available(self, raw_drinks, drink):
        print('Raw Drinks: {}'.format(raw_drinks))
        for drink in drink.get_recipe():
            print('Drink: {}'.format(drink))
            if drink not in raw_drinks: return False
        return True
    def get_available_drinks(self):
        return self.available
    def get_drink_menu(self):
        return self.drink_menu
    def bind_pour_buttons(self, cb):
        self.pour_cb = cb
    def get_pour_params(self, drink_name):
        return self.drink_menu.get_pour_params(drink_name)

class RumCoke:
    def __init__(self):
        self.name = 'Rum and Coke'
        self.recipe = ['Rum', 'Coke']
    def get_name(self):
        return self.name
    def get_recipe(self):
        return self.recipe

class TequilaSunrise:
    def __init__(self):
        self.name = 'Tequila Sunrise'
        self.recipe = ['Tequila', 'Orange Juice']
    def get_name(self):
        return self.name
    def get_recipe(self):
        return self.recipe

class WhiskeyGinger:
    def __init__(self):
        self.name = 'Whisket Ginger'
        self.recipe = ['Whiskey', 'Ginger Ale']
    def get_name(self):
        return self.name
    def get_recipe(self):
        return self.recipe

class Margarita:
    def __init__(self):
        self.name = 'Margarita'
        self.recipe = ['Margarita Mix', 'Tequila']
    def get_name(self):
        return self.name
    def get_recipe(self):
        return self.recipe

class DrinkMakeMenu(GridLayout):
    def __init__(self, **kwargs):
        super(DrinkMakeMenu, self).__init__(cols=2, size_hint=(1,0.8),pos_hint={"left":1, "top":1})
        self.drink_entries = {}
    def reload_menu(self, drinks):
        self.clear_widgets()
        self.drinks = drinks
        self.drink_entries = {}
        for recipe in self.drinks:
            print('Recipe: {}'.format(recipe)) # Recipe object
            self.drink_entries[recipe.get_name()] = DrinkEntry(recipe=recipe)
            self.add_widget(self.drink_entries[recipe.get_name()])
    def bind_pour_btn(self, cb):
        for drink_name in self.drink_entries:
            drink_entry = self.drink_entries[drink_name]
            drink_entry.bind_btn_cb(cb)
    def get_pour_params(self, drink_name):
        return self.drink_entries[drink_name].pour_params()


class DrinkEntry(GridLayout):
    def __init__(self, **kwargs):
        super(DrinkEntry, self).__init__(cols=1, rows=3)
        self.quantity = 0
        
        self.recipe = kwargs['recipe'] # Recipe object
        self.add_widget(Label(text=self.recipe.get_name())) # Drink Name Label
        
        quan_buttons = GridLayout(rows=1, cols=2) # More and less quantity buttons
        self.up_button = Button(text='^^^', on_press = self.inc_quan)
        self.down_button = Button(text='vvv', on_press = self.dec_quan)
        quan_buttons.add_widget(self.down_button)
        quan_buttons.add_widget(self.up_button)
        
        pour_options = GridLayout(cols=2, rows=2) # 2x2 Grid goes in the middle
        self.slider = Slider(min=0, max=100, value=50, on_touch_move=self.update_slider)
        self.slider_label = Label(text='{}% Alk'.format(self.slider.value))
        self.quan_label = Label(text=str(self.quantity))
        pour_options.add_widget(self.slider_label)
        pour_options.add_widget(self.quan_label)
        pour_options.add_widget(self.slider)
        pour_options.add_widget(quan_buttons)
        
        self.add_widget(pour_options)
        self.button = DrinkPourButton(text='Pour Drink', recipe=self.recipe)
        self.add_widget(self.button)
    def bind_btn_cb(self, cb):
        self.button.bind_cb(cb)
    def update_slider(self, instance, arg):
        self.slider_label.text = '{}% Alk'.format(int(self.slider.value))
    def inc_quan(self, instance):
        self.quantity += 1
        self.quan_label.text = str(self.quantity)
    def dec_quan(self, instance):
        if self.quantity == 0: return
        self.quantity -= 1
        self.quan_label.text = str(self.quantity)
    def pour_params(self):
        return [self.recipe.get_recipe(), self.slider.value, self.quantity]
        

class DrinkPourButton(Button):
    def __init__(self, **kwargs):
        super(DrinkPourButton, self).__init__(**kwargs)
        recipe = kwargs['recipe']
        self.drink_list = []
        drink_list = recipe.get_recipe()
        self.recipe_name = recipe.get_name()
        for ingredient in drink_list:
            self.drink_list.append(ingredient)
    def bind_cb(self, cb):
        self.bind(on_press=cb)
