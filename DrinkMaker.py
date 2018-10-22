from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.app import App
from DrinkConstants import *

class Menu:
    def __init__(self):
        self.drinks = [RumCoke(), TequilaSunrise(), WhiskeyGinger(), Margarita()]
        self.drink_menu = DrinkMakeMenu()
        self.rail_menu = RailMenu()
        self.pour_cb = None
        self.active_rail = None
        self.rail_drink_list = RailDrinkList()
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
    def get_rail_drink_menu(self):
        return self.rail_drink_list
    def bind_pour_buttons(self, cb):
        self.pour_cb = cb
    def get_pour_params(self, drink_name):
        return self.drink_menu.get_pour_params(drink_name)
    def bind_rail_buttons(self, change_drink_cb, pour_cb):
        self.rail_menu.bind_buttons(change_drink_cb, pour_cb)
    def set_active_rail(self, new_rail):
        self.active_rail = new_rail
    def get_active_rail(self):
        return self.active_rail
    def change_rail_drink(self, new_drink):
        self.rail_menu.change_drink(self.active_rail, new_drink)
        self.active_rail = None
    def get_rail_menu(self):
        return self.rail_menu
    def reload_rail_list(self, drink_list, change_rail_cb):
        self.rail_drink_list.reload_list(self.active_rail, drink_list, change_rail_cb)
    def get_rail_pour_params(self):
        return self.rail_menu.get_pour_params()

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
        super(DrinkMakeMenu, self).__init__(cols=2,
            #size_hint=(1,0.8),
            #pos_hint={"left":1, "top":1},
        )
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

class RailMenu(GridLayout):
    def __init__(self, **kwargs):
        super(RailMenu, self).__init__(cols=1,rows=4)
        self.alk = 'Choose A Drink!'
        self.mixer = 'Choose A Drink!'
        self.alk_quan = 0
        self.mix_quan = 0

        self.alk_label = Label(text=self.alk)
        self.mixer_label = Label(text=self.mixer)
        self.alk_change_btn = Button(
            text='Change Alcohol',
            font_size=30,
        )
        self.mix_change_btn = Button(
            text='Change Mixer',
            font_size=30,
        )
        self.pour_rail_btn = Button(text='POUR', font_size=44)

        layout = GridLayout(cols=2,rows=2)
        layout.add_widget(self.alk_label)
        layout.add_widget(self.mixer_label)
        layout.add_widget(self.alk_change_btn)
        layout.add_widget(self.mix_change_btn)
        
        quan_layout = GridLayout(rows=2,cols=2)
        self.alk_quan_label = Label(text=str(self.alk_quan))
        self.mix_quan_label = Label(text=str(self.mix_quan))
        alk_button_layout = GridLayout(rows=1,cols=2)
        mix_button_layout = GridLayout(rows=1,cols=2)
        self.alk_quan_up = Button(text='^^^', on_press=self.inc_alk_quan)
        self.mix_quan_up = Button(text='^^^', on_press=self.inc_mix_quan)
        self.alk_quan_down = Button(text='vvv', on_press=self.dec_alk_quan)
        self.mix_quan_down = Button(text='vvv', on_press=self.dec_mix_quan)
        alk_button_layout.add_widget(self.alk_quan_up)
        alk_button_layout.add_widget(self.alk_quan_down)
        mix_button_layout.add_widget(self.mix_quan_up)
        mix_button_layout.add_widget(self.mix_quan_down)
        quan_layout.add_widget(self.alk_quan_label)
        quan_layout.add_widget(self.mix_quan_label)
        quan_layout.add_widget(alk_button_layout)
        quan_layout.add_widget(mix_button_layout)

        self.add_widget(Label(text='Make Your Own Rail!', font_size=44))
        self.add_widget(layout)
        self.add_widget(quan_layout)
        self.add_widget(self.pour_rail_btn)
        
    def bind_buttons(self, change_drink_cb, pour_cb):
        self.alk_change_btn.bind(on_press=change_drink_cb)
        self.mix_change_btn.bind(on_press=change_drink_cb)
        self.pour_rail_btn.bind(on_press=pour_cb)
    def change_drink(self, active, new_drink):
        if 'Alcohol' in active: 
            self.alk_label.text=new_drink
            self.alk = new_drink
        else: 
            self.mixer_label.text=new_drink
            self.mixer = new_drink
    def inc_alk_quan(self, instance):
        self.alk_quan += 1
        self.alk_quan_label.text=str(self.alk_quan)
    def dec_alk_quan(self, instance):
        if self.alk_quan != 0: self.alk_quan -= 1
        self.alk_quan_label.text=str(self.alk_quan)
    def inc_mix_quan(self, instance):
        self.mix_quan += 1
        self.mix_quan_label.text=str(self.mix_quan)
    def dec_mix_quan(self, instance):
        if self.mix_quan != 0: self.mix_quan -= 1
        self.mix_quan_label.text=str(self.mix_quan)
    def get_pour_params(self):
        return_val = {}
        if self.alk != 'Choose A Drink!' and self.alk_quan != 0:
            return_val[self.alk] = self.alk_quan
        if self.mixer != 'Choose A Drink!' and self.mix_quan != 0:
            return_val[self.mixer] = self.mix_quan
        return return_val



class RailDrinkList(GridLayout):
    def __init__(self, **kwargs):
        super(RailDrinkList, self).__init__(cols=2, size_hint=(1, 0.8), pos_hint={"left":1, "top":1})
    def reload_list(self, active, drink_list, press_cb):
        self.clear_widgets()
        if 'Alcohol' in active: is_alk = True
        else: is_alk = False
        for drink in drink_list:
            if is_alk and drink in ALK_MENU: 
                self.add_widget(Button(text=drink, on_press=press_cb, background_color = [1,0,0,.75]))
            elif not is_alk and drink in MIXER_MENU: self.add_widget(Button(text=drink, on_press=press_cb, background_color = [0,1,0,.75]))
        
        
        
        
        
        
        
        
        
        
        
        