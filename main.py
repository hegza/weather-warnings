#!/usr/bin/env python

import signals
import owm
import sys, time
import json
from time import sleep
from messages import *

DEMO = False
UPDATE_FREQ_MIN = 15
 
def init():
	signals.deactivate("rain")
	print GREETING(UPDATE_FREQ_MIN)

## This function updates LED status
def step():
	print UPDATE_MSG(time.time())

	## Get the weather and the forecast online
	weather, forecast = owm.get_weather_now()

	weather_rain = 0.0
	try:
		weather_rain = weather["rain"]["3h"]
	
		## This could be used to light up another LED	
		if (weather_rain >= 1): pass
		else: pass

	except: pass ## No rain in the last 3 hrs

	print "Millis of rain within the last 3 h: " + str(weather_rain)
	

	if ("list" in forecast and len(forecast["list"]) > 2):
		## HACK: take the 1st, 2nd and 3rd value, that *should* usually be the 0 to 9 hours forecast
		## TODO: parse the 'dt' field and find out which times match best with what we're looking for
		rain_forecast_0 = 0.0
		rain_forecast_3 = 0.0
		rain_forecast_6 = 0.0
		try:
			## Rain in 0 to 3 hrs
			rain_forecast_0 = forecast["list"][0]["rain"]["3h"]
		except: pass
		try:
			## Rain in 3 to 6 hrs
			rain_forecast_3 = forecast["list"][1]["rain"]["3h"]
		except: pass
		try:
			## Rain in 6 to 9 hrs
			rain_forecast_6 = forecast["list"][2]["rain"]["3h"]
		except: pass

		if (DEMO):
			rain_forecast_3 += 5

		print "Rain amounts for the 0..3, 3..6, and 6..9 h ranges: " + str(rain_forecast_0) + " " + str(rain_forecast_3) + " " + str(rain_forecast_6) + " (mms)"

		if (rain_forecast_0 >= 0.65 or rain_forecast_3 >= 0.75 or rain_forecast_6 >= 0.85):
			update_led("rain", True, "Forecast: rain in the next 9 hours.")
		else:
			update_led("rain", False, "Forecast: no rain in the next 9 hours.")

	else:
		print "ERR: There's something wrong with how I'm trying to parse the response from api.openweathermap.org. JSON: " + json.dumps(forecast)

	print ""

## This function gets run when the application is started
def run():
	init()
	while (True):
		## Execute logic
		step()
		## Wait for UPDATE_FREQ_MIN minutes
		sleep(UPDATE_FREQ_MIN * 60)


def update_led(led_name, enable, message):
	if enable:
		print message + " Turning LED \"" + led_name + "\" on..."
		if (not signals.is_active(led_name)):
			signals.activate(led_name)
	else:
		print message + " Turning LED \"" + led_name + "\" off..."
		if (signals.is_active(led_name)):
			signals.deactivate(led_name)

run()

