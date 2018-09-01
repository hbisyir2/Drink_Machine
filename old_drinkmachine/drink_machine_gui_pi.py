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
shotNum = 0

class DrinkApp(App):
	
	def build(self):
		global ozNum
		layout = FloatLayout()
		
		def shotMinus(event):
			global shotNum
			if shotNum > 0:
				shotNum -= 1
				shotValue.text = str(shotNum)
				
		def shotPlus(event):
			global shotNum
			if shotNum < 10:
				shotNum += 1
				shotValue.text = str(shotNum)
		
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
				
		def PourShot(event):
			global shotNum
			shotNum = 0
			shotValue.text = str(shotNum)
			
		def PourMix(event):
			global ozNum
			ozNum = 0
			ozValue.text = str(ozNum)
			
		def PourBoth(event):
			global ozNum, shotNum
			ozNum = 0
			shotNum = 0
			ozValue.text = str(ozNum)
			shotValue.text = str(shotNum)
			
		def mixTapRelease(event):
			global shotNum
			if mixToggle.state == 'down':
				shotNum += 1
				#start pouring mixer
			else:
				shotNum += 1
				#stop pouring mixer
			shotValue.text = str(shotNum)
			
		def shotTapRelease(event):
			global shotNum
			if shotToggle.state == 'down':
				shotNum += 1
				#start pouring shot
			else:
				shotNum += 1
				#stop pouring shot
			shotValue.text = str(shotNum)
			
		def bothTapRelease(event):
			global shotNum
			if bothToggle.state == 'down':
				shotNum += 1
				# start pouring both
			else:
				shotNum += 1
				#stop pouring both
			shotValue.text = str(shotNum)

		mixButton = Button(
			text='Pour Mixer', 
			font_size=14,
			size_hint = (.33, .1),
			pos=(30,200),
			on_press = PourMix)
			
		shotButton = Button(
			text='Pour Shots', 
			font_size=14,
			size_hint = (.33, .1),
			pos=(490,200),
			on_press = PourShot)
			
		bothButton = Button(
			text='Pour Both', 
			font_size=14,
			size_hint = (.21, .1),
			pos=(307,200),
			on_press = PourBoth)

		mixToggle = ToggleButton(
			text='TAP',
			font_size=45,
			size_hint = (.33, .25),
			pos=(30,50),
			on_release = mixTapRelease)
			
		shotToggle = ToggleButton(
			text='TAP',
			font_size=45,
			size_hint = (.33, .25),
			pos=(490,50),
			on_release = shotTapRelease)
			
		bothToggle = ToggleButton(
			text='TAP',
			font_size=45,
			size_hint = (.21, .25),
			pos=(307,50),
			on_release = bothTapRelease)
			
		mixerLabel = Label(
			text='MIXER',
			font_size = 50,
			color = (0,0,0,1),
			pos=(-245,180))
			
		shotLabel = Label(
			text='SHOTS',
			font_size = 50,
			color = (0,0,0,1),
			pos=(220,180))
			
		ozUpButton = Button(
			text='>',
			font_size=24,
			size_hint = (.08,.08),
			pos=(230, 300),
			on_press = ozPlus)
			
		shotUpButton = Button(
			text='>',
			font_size=24,
			size_hint = (.08,.08),
			pos=(688, 300),
			on_press = shotPlus)
		
		ozDownButton = Button(
			text='<',
			font_size=24,
			size_hint = (.08,.08),
			pos=(30, 300),
			on_press = ozMinus)
			
		shotDownButton = Button(
			text='<',
			font_size=24,
			size_hint = (.08,.08),
			pos=(488, 300),
			on_press = shotMinus)
			
		ozValue = Label(
			text = str(ozNum),
			font_size = 60,
			color = (0,0,0,1),
			pos=(-240,75))
			
		shotValue = Label(
			text = str(shotNum),
			font_size = 60,
			color = (0,0,0,1),
			pos=(220,75))
		
		layout.add_widget(mixButton)
		layout.add_widget(shotButton)
		layout.add_widget(bothButton)
		layout.add_widget(mixToggle)
		layout.add_widget(shotToggle)
		layout.add_widget(bothToggle)
		layout.add_widget(mixerLabel)
		layout.add_widget(shotLabel)
		layout.add_widget(ozUpButton)
		layout.add_widget(shotUpButton)
		layout.add_widget(ozDownButton)
		layout.add_widget(shotDownButton)
		layout.add_widget(ozValue)
		layout.add_widget(shotValue)
		
		return layout

if __name__ == '__main__':
	DrinkApp().run()
