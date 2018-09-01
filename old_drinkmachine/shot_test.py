import RPi.GPIO as GPIO
import time

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

alk_enable = 19
alk_motor = 23

mix_enable = 22
mix_motor = 16

def PourShot():
	numShot = input('Enter number of shots: ')
	try:
		numShot = int(numShot)
	except:
		print('Please enter a number')
		return
	GPIO.output(alk_enable, GPIO.HIGH)
	GPIO.output(alk_motor, GPIO.HIGH)
	timeSleep = numShot*11.5
	time.sleep(timeSleep)
	GPIO.output(alk_enable, GPIO.LOW)
	GPIO.output(alk_motor, GPIO.LOW)

def PourMix():
	emptyVar = input('press ENTER to start pouring Mixer')
	GPIO.output(mix_enable, GPIO.HIGH)
	GPIO.output(mix_motor, GPIO.HIGH)
	emptyVar = input('press ENTER to stop pouring')
	GPIO.output(mix_enable, GPIO.LOW)
	GPIO.output(mix_motor, GPIO.LOW)
	
try:
	while True:
		PourShot()
		PourMix()
except:
	print('Exiting program...')
	GPIO.cleanup()
