# Integrator

## Files, and what they do/are:
### Code
+ main.py
The main file. This is where execution starts.
It mostly contains web/Flask related code, as-is.

+ necu.py
The NECU 'banking driver'. It drives Selenium, which
tells PhantomJS how to log into and scrape NECU's website
for banking information.

+ cache.py
A small library file that contains the classes Cache, Frame,
and Account. These store information collected by banking drivers,
into classes that allow structured, easy access to them and their
information.

+ weather.py
The weather driver. Fetches (or at least will fetch) weather information
from the service OpenWeatherMap.

### Templates, etc.:
+ templates/home.html
The HTML code for the home page.

### Other:
+ .gitignore
If you're unfamiliar, this marks files that should not be staged/committed
in a git repository. These are files that I've had pop into existence here
that I would really prefer wouldn't, for one reasons or another.

+ README.md
*squints*
