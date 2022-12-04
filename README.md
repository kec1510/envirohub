# EnviroHub: A Content Platform for Climate Enthusiasts

Welcome to EnviroHub, a content aggregator for climate and environment enthusiasts. Through this platform, you can search the latest climate news and generate weather and air quality forecasts by location!

## EnviroHub Installation and Launch

To run EnviroHub on your local computer, you will first need to [install Python](https://www.python.org/downloads/). Then, clone the [EnviroHub GitHub repository](https://github.com/kec1510/envirohub) (via `git clone` if you have git installed, or via ZIP download).

Open a terminal window within the repository folder and execute `pip install -r requirements.txt` to install the necessary dependencies. Finally, execute `python app.py` to launch EnviroHub in your browser.

## Using EnviroHub

Once you have successfully launched EnviroHub, register for an account at the `/register` route. Note the validation information displayed on the page (i.e. the required username and password length).

Upon successful registration, you will be redirected to the login page. Once you enter your credentials in the login form, you will gain access to your very own EnviroHub Dashboard. The Dashboard contains forecast information for Cambridge, MA (where the project was created), but you can generate a custom forecast for any location by navigating to the Forecasts page and entering the latitude and longitude of your desired location. The History page will save all of your custom forecasts in a table sorted by the latest forecast.

The Dashboard also contains the latest news headlines along with their URLs, publish dates, and sources for the search query `climate change`. You can generate your own news article results by navigating to the News page and entering a query of your choice.
