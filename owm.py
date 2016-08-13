import requests
import time
import json

CACHE_UPDATE_FREQ_MIN = 15


def read_file(filename):
	f = open(filename, 'r')
	return f.read().rstrip('\n\r')
	f.close()

city_id = read_file('data/city_id.txt')
api_key = read_file('data/openweathermap.key')

last_cache_time = 0
cached_weather = ""
cached_forecast = ""

## Make sure the cache files exist
cache_file = open('data/last_weather.cache', 'a+')
cache_file.close()

forecast_cache_file = open('data/last_forecast.cache', 'a+')
forecast_cache_file.close()

def load_cache():	
	global last_cache_time, cached_weather, cached_forecast

	cache_file = open('data/last_weather.cache', 'r')
	forecast_cache_file = open('data/last_forecast.cache', 'r')
	cache_lines = cache_file.readlines()
	forecast_cache_lines = forecast_cache_file.readlines()
	cache_file.close()
	forecast_cache_file.close()

	if (len(cache_lines) != 0):
		last_cache_time = int(cache_lines[0])
		cached_weather = json.loads( cache_lines[1] )

	if (len(forecast_cache_lines) != 0):
		cached_forecast = json.loads( forecast_cache_lines[1] )

		

def save_cache(weather, forecast):
	global last_cache_time, cached_weather
	last_cache_time = int(time.time())
	cached_weather = weather
	cached_forecast = forecast
	fw = open('data/last_weather.cache', 'w')
	fw.write(str(last_cache_time))
	fw.write('\n')
	fw.write(json.dumps(cached_weather))
	fw.close()

	ff = open('data/last_forecast.cache', 'w')
	ff.write(str(last_cache_time))
	ff.write('\n')
	ff.write(json.dumps(cached_forecast))
	ff.close()

load_cache()


def get_weather_now():
	global cached_weather, cached_forecast
	weather_json = None
	forecast_json = None
	if (int(time.time()) >= last_cache_time + CACHE_UPDATE_FREQ_MIN * 60):
		print "Info: Fetching weather data from api.openweathermap.org..."
		online_weather_json = make_request()
		online_forecast_json = make_request_forecast()
		if (online_weather_json != None and online_forecast_json != None):
			save_cache(online_weather_json, online_forecast_json)
		load_cache()
	else:
		print "Info: Returning weather cached at " + time.strftime('%H:%M:%S %d.%m.%Y', time.localtime(last_cache_time)) + "..."
		print "Info: next cache update will be at: " + time.strftime('%H:%M:%S %d.%m.%Y', time.localtime(last_cache_time + CACHE_UPDATE_FREQ_MIN * 60))

	weather_json = cached_weather
	forecast_json = cached_forecast
	return weather_json, cached_forecast

def make_request():
	url = 'http://api.openweathermap.org/data/2.5/weather?id=%s&APPID=%s' % (city_id, api_key)
	## url = 'http://api.openweathermap.org/data/2.5/weather?lat=%d&lon=%d&APPID=%s' % (24, 61, api_key)
	print "Info: sending request to " + url
	try:
		r = requests.get( url )
		weather_json = json.loads(r.text)
		## print "Info: Response: " + json.dumps(r.text)

	except:
		weather_json = None
	return weather_json

def make_request_forecast():	
	## url = 'http://api.openweathermap.org/data/2.5/forecast?id=%s&APPID=%s' % (city_id, api_key) ## Can't use this for some reason. Returns no data on Pohjois-Hervanta.
	url = 'http://api.openweathermap.org/data/2.5/forecast?lat=%f&lon=%f&APPID=%s' % (61.457722, 23.847111, api_key)
	print "Info: sending request to " + url
	try:
		r = requests.get( url )
		forecast_json = json.loads(r.text)
		## print "Info: Response: " + json.dumps(r.text)

	except:
		forecast_json = None
	return forecast_json

