
from gpiozero import LED

RAIN = "rain"
RAIN_LATER = "rain_later"
leds = {RAIN: LED(4) }##, RAIN_LATER: LED(5)}

def activate(key):
	try:
		leds[key].on()
	except:
		print "Warning: LED is probably disconnected"

def deactivate(key):
	try:
		leds[key].off()
	except:
		print "Warning: LED is probably disconnected"

def is_active(key):
	try:
		return leds[key].is_active
	except:
		pass

