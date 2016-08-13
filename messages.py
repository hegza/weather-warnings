import time

def GREETING(update_interval):
	ret_str = ""	
	ret_str += "## Initializing the weather app\n"
	ret_str += "LED status will be updated every " + str(update_interval) + " minutes.\n"
	return ret_str

def UPDATE_MSG(epoch):
	ret_str = ""
	ret_str += "## Updating weather and LED status...\n"
	ret_str += "" + time.strftime('%H:%M:%S %d.%m.%Y', time.localtime(epoch)) + " (" + str(epoch) + ")\n"
	return ret_str

