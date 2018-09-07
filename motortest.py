# pin 6 connect to all 4 grounds (4,5,12,13)
# pin 1 to 16 (5V power)
# pin 16 to 7 (driver input 2)
# pin 18 to 2 (driver input 1)
# pin 22 to 1 (1, 2 driver enable)
# 6V DC connection to 8 (DC power)
# battery connection to common ground

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

#mode = {16: 'low', 18: 'low', 22: 'low', 19: 'low', 21: 'low', 23: 'low'}
#pins = [16,18,22,19,21,23]

pins = [11,13,15,16,18,22]


mode = {}
for pin in pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)
	mode[pin] = 'high'

print('Enter number to make output high')
print('Enter negative number to make output low')
print('Pins: {}'.format(pins))
print('Enter 0 to exit program')

try:
	while True:
		for pin in pins:
			print('Pin {}: {}'.format(pin, mode[pin]))
		pinInput = int(input('\n\nEnter pin value to set output: '))
		if abs(pinInput) not in pins and pinInput != 0: 
			print('Must enter pin number in {}'.format(pins))
		elif pinInput > 0:
			print('Making pin {} output HIGH'.format(pinInput))
			GPIO.output(pinInput, GPIO.HIGH)
			mode[pinInput] = 'high'
		elif pinInput < 0:
			pinInput = abs(pinInput)
			print('Making pin {} output LOW'.format(pinInput))
			GPIO.output(pinInput, GPIO.LOW)
			mode[pinInput] = 'low'
		else:
			break
except Exception as err:
	print('Caught exception: {}'.format(err))
finally:
	print('exiting program...')
	GPIO.cleanup()
