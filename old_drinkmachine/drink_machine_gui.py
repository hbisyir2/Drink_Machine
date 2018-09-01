import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.floatlayout import FloatLayout

Window.clearcolor = (.8, .8, .8, 1)

ozNum = 0

class DrinkApp(App):
	
	def build(self):
		global ozNum
		layout = FloatLayout()
		
		def ozMinus(event):
			global ozNum
			if ozNum > 0:
				ozNum -= 1
				ozValue.text = str(ozNum)
		
		def ozPlus(event):
			global ozNum
			if ozNum < 10:
				ozNum += 1
				ozValue.text = str(ozNum)
		

		mixButton = Button(
			text='Pour Mixer', 
			font_size=14,
			size_hint = (.4, .1),
			pos=(30,200))

		mixToggle = ToggleButton(
			text='TAP',
			font_size=45,
			size_hint = (.4, .25),
			pos=(30,50))
			
		mixerLabel = Label(
			text='MIXER',
			font_size = 50,
			color = (0,0,0,1),
			pos=(-210,180))
			
		ozUpButton = Button(
			text='>',
			font_size=24,
			size_hint = (.08,.08),
			pos=(250, 300),
			on_press = ozPlus)
		
		ozDownButton = Button(
			text='<',
			font_size=24,
			size_hint = (.08,.08),
			pos=(50, 300),
			on_press = ozMinus)
			
		ozValue = Label(
			text = str(ozNum),
			font_size = 60,
			color = (0,0,0,1),
			pos=(-220,75))
		
		layout.add_widget(mixButton)
		layout.add_widget(mixToggle)
		layout.add_widget(mixerLabel)
		layout.add_widget(ozUpButton)
		layout.add_widget(ozDownButton)
		layout.add_widget(ozValue)
		
		return layout

if __name__ == '__main__':
	DrinkApp().run()
