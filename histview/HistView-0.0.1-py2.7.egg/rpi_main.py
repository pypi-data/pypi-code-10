import kivy
kivy.require('1.0.6') 

import time
import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty


import RPi.GPIO as GPIO
import Adafruit_MAX31855.MAX31855 as MAX31855


# Set up GPIO:
GPIO.setmode(GPIO.BCM)
Heater = 6
GPIO.setup(Heater, GPIO.OUT)
GPIO.output(Heater, True)

AutoFill = 23
GPIO.setup(AutoFill, GPIO.OUT)
GPIO.output(AutoFill, True)

Fan = 24
GPIO.setup(Fan, GPIO.OUT)
GPIO.output(Fan, True)

Swap = 25
GPIO.setup(Swap, GPIO.OUT)
GPIO.output(Swap, True)

AlcholFan = 5 
GPIO.setup(AlcholFan, GPIO.OUT)
GPIO.output(AlcholFan, True)

Float = 12
GPIO.setup(Float, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#Temps
TC_Clk = 18
TC_DO = 4
Pot_CS = 17
Head1_CS = 27
Head2_CS = 22

Pot =   MAX31855.MAX31855(TC_Clk, Pot_CS,   TC_DO)
Head1 = MAX31855.MAX31855(TC_Clk, Head1_CS, TC_DO)
Head2 = MAX31855.MAX31855(TC_Clk, Head2_CS, TC_DO)

Head1Temp = Head1.readTempC()



# Define some helper functions:
def press_callback(obj):
	print("Button pressed,", obj.text)
	if obj.text == 'BEEP!':
		# turn on the beeper:
		GPIO.output(beepPin, GPIO.HIGH)
		# schedule it to turn off:
		Clock.schedule_once(buzzer_off, .1)
	if obj.text == 'Heater':
		if obj.state == "down":
			print ("button on")
			GPIO.output(Heater, False)
		else:
			print ("button off")
			GPIO.output(Heater, True)

	if obj.text == 'AutoFill':
		if obj.state == "down":
			print ("button on")
			GPIO.output(AutoFill, False)
		else:
			print ("button off")
			GPIO.output(AutoFill, True)

	if obj.text == 'AlcholFan':
		if obj.state == "down":
			print ("button on")
			GPIO.output(AlcholFan, False)
		else:
			print ("button off")
			GPIO.output(AlcholFan, True)

	if obj.text == 'Swap':
		if obj.state == "down":
			print ("button on")
			GPIO.output(Swap, False)
		else:
			print ("button off")
			GPIO.output(Swap, True)		

	if obj.text == 'Fan':
		if obj.state == "down":
			print ("button on")
			GPIO.output(Fan, False)
		else:
			print ("button off")
			GPIO.output(Fan, True)		

	if obj.text == 'Head1':
			Head1Temp = Head1.readTempC()
			print 'Head1: {0:0.1F}'.format(Head1Temp)


# Modify the Button Class to update according to GPIO input:
# This is my attempt at updating Head1 Temp on a button press, leaving it here to use for later if needed. 
class Head1Control(Label):
	display_text = StringProperty("Head1: {0:0.1F}".format(Head1Temp))
	def update(self):
		time.sleep(2)
		self.display_text = "Head1: {0:0.1F}".format(Head1Temp)


class MyApp(App):   		

	def build(self):
		# Set up the layout:
		layout = GridLayout(cols=3, spacing=30, padding=30, row_default_height=150)

		# Make the background gray:
		with layout.canvas.before:
			Color(.2,.2,.2,1)
			self.rect = Rectangle(size=(800,600), pos=layout.pos)

		# Create the rest of the UI objects (and bind them to callbacks, if necessary):
		heaterControl = ToggleButton(text="Heater")
		heaterControl.bind(on_press=press_callback)
		autofillControl = ToggleButton(text="AutoFill")
		autofillControl.bind(on_press=press_callback)
		alcholfanControl = ToggleButton(text="AlcholFan")
		alcholfanControl.bind(on_press=press_callback)
		swapControl = ToggleButton(text="Swap")
		swapControl.bind(on_press=press_callback)
		fanControl = ToggleButton(text="Fan")
		fanControl.bind(on_press=press_callback)
		Head1Control = Label(text="Head1: {0:0.1F}".format(Head1Temp))


		# These are the UI elements to the layout:
		layout.add_widget(heaterControl)
		layout.add_widget(autofillControl)
		layout.add_widget(fanControl)
		layout.add_widget(swapControl)
		layout.add_widget(alcholfanControl)
		layout.add_widget(Head1Control)

		return layout

if __name__ == '__main__':
	MyApp().run()
