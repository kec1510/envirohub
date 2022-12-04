# EnviroHub: Design Choices

## Frontend

The platform's frontend is run on Flask. The interface is an adapted version of Bootstrap's [SB-Admin template](https://startbootstrap.com/template/sb-admin) and contains HTML, CSS, Javascript integrated with Flask and Jinja2. I chose to adapt this template because it provides a clean, well-organized, minimalist dashboard and is well-suited to enable EnviroHub's content aggregation. The template also provides datatable functionality that allows users to easily search through the table, sort the table's rows, and paginate through the table's results.

## Backend

The backend functionality is implemented in Python with a SQLite database. The database is stored in the `envirohub.db` file, and the API-calling source code can be found in the `programs` directory.

### Database

EnviroHub's SQLite database contains platform users' account information in the `users` table as well as the history of forecasts they've requested through EnviroHub in the `fc_history` table. The full schema used to initialize the database can be found in `schema.sql`.

### News Functionality

For the news search functionality, I used the `requests` library to call [NewsAPI](https://newsapi.org/docs) and The New York Times' [Article Search API](https://developer.nytimes.com/docs/articlesearch-product/1/overview). I then synthesized these outputs to provide EnviroHub users with the following information on each news article: its headline, URL, the date it was published, and its source. I used Jinja2's `urlize()` function to make the URLs clickable when displayed in the Flask interface.

### Forecast Functionality

I used `requests` to call the [Open-Meteo Weather Forecast API](https://open-meteo.com/en/docs) for the forecast functionality.
