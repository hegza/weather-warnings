# weather-warnings
A small Internet weather app with GPIO LED's for Raspberry Pi, implemented
using Python 2.7.8.

The application polls the [openweathermap](https://openweathermap.org/) api and lights up a LED if it's going to
be raining in the next few hours.


## Installation

Examples provided using archlinux with pacman. NB: the default linux OS on 
the Raspberry Pi that I used for the project had some libraries related to 
GPIO control. This software may not function properly without them.

1. Install Python 2 (tested with 2.7.8)
```
pacman -S python2
```
2. Install pip for Python 2
```
pacman -S python2-pip
```
3. Install the gpiozero module using pip
```
pip2 install gpiozero
```

## Configuration
- Add your openweathermap API key to data/openweathermap.key
- Add your openweathermap city-id to data/city_id.txt
	* You can get the city-id from the openweathermap site
	* NB: There's one hardcoded location in owm.py line 104. You may want to
	change this to point to your local geo-coordinate. Sorry for the inconvenience!


## Notes on the target platform

The LED used for the example was attached to the GPIO pin with index 4. Due to
the small scope of the project, a separate config was deemed unnecessary. This
can be reconfigured fairly easily from the source file signals.py. Again, Sorry
for the inconvenience!

