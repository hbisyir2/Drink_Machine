# pin 6 connect to all 4 grounds (4,5,12,13)
# pin 1 to 16 (5V power)
# pin 16 to 7 (driver input 2)
# pin 18 to 2 (driver input 1)
# pin 22 to 1 (1, 2 driver enable)
# 6V DC connection to 8 (DC power)
# battery connection to common ground

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

GPIO.output(16, GPIO.LOW)
GPIO.output(18, GPIO.LOW)
GPIO.output(22, GPIO.LOW)

GPIO.output(19, GPIO.LOW)
GPIO.output(21, GPIO.LOW)
GPIO.output(23, GPIO.LOW)

mode = {16: 'low', 18: 'low', 22: 'low', 19: 'low', 21: 'low', 23: 'low'}

print('Enter number to make output high')
print('Enter negative number to make output low')
print('Enter 0 to exit program')

try:
	while True:
		print('\n16: ' + mode[16] + '\n18: ' + mode[18] + '\n22: ' + mode[22])
		print('\n19: ' + mode[19] + '\n21: ' + mode[21] + '\n23: ' + mode[23])
		pinInput = input('\n\nEnter which pin to make output high: ')
		pinInput = int(pinInput)
		if pinInput != 16 and pinInput != 18 and pinInput != 22 and pinInput != -16 and pinInput != -18 and pinInput != -22 and pinInput != 0 and pinInput != 19 and pinInput != 21 and pinInput != 23 and pinInput != -19 and pinInput != -21 and pinInput != -23:
			print('Must be pin 16, 18, 22, 19, 21, or 23')
		elif pinInput > 0:
			print('Making pin ' + str(pinInput) + ' output HIGH')
			GPIO.output(pinInput, GPIO.HIGH)
			mode[pinInput] = 'high'
		elif pinInput < 0:
			pinInput = abs(pinInput)
			print('Making pin ' + str(pinInput) + ' output LOW')
			GPIO.output(pinInput, GPIO.LOW)
			mode[pinInput] = 'low'
		else:
			break
except:
	print('exiting program...')
	GPIO.cleanup()
	
finally:
	print('exiting program...')
	GPIO.cleanup()