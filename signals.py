
from gpiozero import LED

RAIN = "rain"
RAIN_LATER = "rain_later"
leds = {RAIN: LED(4) }##, RAIN_LATER: LED(5)}

def activate(key):
	leds[key].on()

def deactivate(key):
	leds[key].off()

def is_active(key):
	return leds[key].is_active

