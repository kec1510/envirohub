# EnviroHub: A Content Platform for Climate Enthusiasts

Welcome to EnviroHub, a content aggregator for climate and environment enthusiasts. Through this platform, you can search the latest climate news and generate weather and air quality forecasts by location!

## EnviroHub Installation and Launch

To run EnviroHub on your local computer, you will first need to [install Python](https://www.python.org/downloads/). Then, clone the [EnviroHub GitHub repository](https://github.com/kec1510/envirohub) via `git clone` if you have git installed, or via ZIP download (if reading this documentation from CS50, you should already have all the necessary files).

Open a terminal window within the repository folder and execute `pip install -r requirements.txt` to install the necessary dependencies. Finally, execute `python app.py` to launch EnviroHub in your browser.

## Using EnviroHub

Once you have successfully launched EnviroHub, register for an account on the `Register` page. Note the validation information displayed on the page (i.e. the required username and password length). Upon successful registration, you will be redirected to the `Login` page. Once you enter your credentials in the login form, you will gain access to your very own EnviroHub Dashboard (the EnviroHub logo on the navigation bar redirects back to this Dashboard).

The Dashboard contains forecast information for Cambridge, MA (where the project was created). You can generate a custom forecast for any location by navigating to the `Forecasts` page and entering the latitude and longitude coordinates of your desired location. Upon clicking `Get Forecast`, the page will display a forecast for your coordinates in the same format as the forecast in the Dashboard. The `New Forecast` button redirects you back to the initial latitude and longitude form.

All of your custom forecasts are saved in EnviroHub's database. The `History` page will display these forecasts in a table sorted by the latest forecast, displaying the datetime, latitude/longitude, temperature, weather, and air quality index for each forecast.

The Dashboard also contains a table of the latest news headlines along with their URLs, publish dates, and sources for the search query `climate change`. At the top of the table, you can change how many results are displayed per page, and at the bottom of the table you can paginate through the results. You can also sort the table ascending and descending by each column (it may be most relevant to sort by `Date Published`) by clicking on the column name or on the up and down arrows beside the column name. You can generate your own news article results by navigating to the `News` page and entering a query of your choice. Upon clicking `Get Headlines`, the page will display a table of results with the same format and functionality as the table in the Dashboard. The `New Search` button redirects you back to the initial search query form.

To log out of your session, click the `logout` link in the navigation bar, which will redirect you to the `Login` page.

<!-- ## EnviroHub Intro Video

The short intro video for EnviroHub can be found [here](https://youtube.com). -->
