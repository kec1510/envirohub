# EnviroHub: Design Choices

## Frontend

The platform's frontend is run on Flask. The interface is an adapted version of Bootstrap's [SB-Admin template](https://startbootstrap.com/template/sb-admin) and contains HTML, CSS, Javascript integrated with Flask and Jinja2. I chose to adapt this template because it provides a clean, well-organized, minimalist dashboard and is well-suited to enable EnviroHub's content aggregation. The template also provides datatable functionality that allows users to easily search through the table, sort the table's rows, and paginate through the table's results.

The format for EnviroHub's forecasts and data tables are adapted from the SB-Admin template, and can be found in the `index.html` template for the EnviroHub Dashboard as well as in the `forecast-results.html` and `news-results.html` templates.

Lastly, the `scripts.js` and `styles.css` files in the `static` folder were downloaded from the SB-Admin template. Much of the initial CSS was not necessary for EnviroHub, so I filtered through `styles.css` to isolate relevant CSS to the project. The `scripts.js` file includes a jQuery function that enables the datatable formatting and functionality for EnviroHub's data tables (as described above).

## Backend

The backend functionality is implemented in Python with a SQLite database. The database is stored in the `envirohub.db` file, and the API-calling source code can be found in the `programs` directory. The main application file is `app.py`, with additional configuration functions stored in `config.py`.

### Registration and Login/Logout

EnviroHub's registration and login-logout features are an adapted version of the implementation from CS50's Problem Set 9: Finance. Registration and login credential validation are facilitated through the SQLite database's `users` table.

The registration and login forms were initialized as classes using the `WTForms` Python package in order to easily create a minimum username and password length. `WTForms` also streamlines the process of correcting for invalid usernames, passwords, and/or confirmations.

EnviroHub also leverages the `@login_required` decorator from CS50 Finance to allow access to the Dashboard and other relevant routes only after users have successfully logged in.

### Database

EnviroHub's SQLite database contains platform users' account information in the `users` table as well as the history of forecasts they've requested through EnviroHub in the `fc_history` table. The full schema used to initialize the database can be found in `schema.sql`.

### Forecast Functionality

The implementation of the forecast functionality can be found in `programs/forecasts.py`. The `forecasts.py` file includes a `weather_aq_forecast` function which takes in two parameters, latitude and longitude. These parameters allow for the custom forecast feature found on EnviroHub's `Forecast` page, where users can generate their own forecasts by location.

I used `requests` to call the `forecast` endpoint of the [Open-Meteo Weather Forecast API](https://open-meteo.com/en/docs). I decided to use this API because it includes centralized weather and air quality metrics (and the free querying plan was the most robust of the weather APIs I researched). I included temperature, a description of the weather, air quality index, and air pollutant concentrations in the forecast results because these are relevant data points from the Open-Meteo API that give a broad overview of the atmospheric factors at play in a given location. I passed this data into the `index.html` and `forecast_results.html` templates for the Dashboard and custom forecast results respectively.

I also created two `.csv` files, `wmo_codes.csv` and `aqi_indices.csv`. These files match numeric results from the Open-Meteo API with qualitative descriptions that the general public can more easily interpret (i.e. matching numeric World Meteorological Organization codes with their corresponding qualitative weather descriptions, and matching numeric Air Quality Indices with a qualitative characterization of the air quality in the region, like "Very Good", "Fair", or "Poor").

In `app.py`, the `/forecast` route accepts both GET and POST requests. Upon a GET request, `/forecast` displays the `forecasts.html` template containing a simple form with fields to enter latitude and longitude coordinates to generate forecasts for a user's desired location. Upon a POST request, `/forecast` displays the `forecast_results.html` template containing the generated forecast while also storing the forecast in the `fc_history` table of the SQLite database. The platform will throw an error if the latitude and longitude inputs are empty or otherwise invalid.

#### Forecast History

I implemented the `History` page by using the `sqlite3` Python package to select relevant forecast data from the `fc_history` table in the `envirohub.db` SQLite database. I then passed this data into the `history.html` template.

### News Functionality

The implementation of the news search functionality can be found in `programs/news.py`. The `news.py` file includes a `nyt_articles` function which takes in a `query` parameter and a `get_news` function which also takes in a `query` parameter. For these functions, I used the `requests` library to call The New York Times' [Article Search API](https://developer.nytimes.com/docs/articlesearch-product/1/overview) and [NewsAPI](https://newsapi.org/docs) respectively. These functions enable the custom search feature found on EnviroHub's `News` page, where users can generate their own news results by a desired search term.

I decided to include two separate functions because I was working with two separate APIs that generated two different response bodies. Since the keys and values associated with the information I wanted to extract for each article differed between these APIs, I decided it would be best to compartmentalize the data extraction process into two functions.

The `get_news` function ultimately synthesizes the outputs from the two APIs to provide EnviroHub users with the following information on each news article: its headline, URL, the date it was published, and its source.  I passed this data into the `index.html` and `news_results.html` templates for the Dashboard and custom news search results respectively. I used Jinja2's `urlize` function to make all articles' URLs clickable when displayed on the platform.

### Additional Design Choices

I created custom error templates for 400 (Bad Request) and 404 (Page Not Found) errors in the `templates` folder. The `app.py` file includes a custom error handler for 404 errors to ensure that the custom 404 error page is displayed. The custom error templates include the EnviroHub navigation bar to ensure that users can easily navigate back to the Dashboard or to the Registration/Login pages.

I also included the tree favicon for the platform as well as the leaves on the Dashboard to provide some greenery (consistent with the climate and environment theme).
