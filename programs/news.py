import requests as req

from programs.keys import NYT, NewsAPI

def nyt_articles(query):
    data = []
    # Paginates through the NYT Article Search API's results three times for a total of 30 headlines
    for i in range(3):
        # Queries the NYT Article Search API's Energy, Environment, and Climate
        # news desks to ensure the most environmentally relevant results.
        # Also sorts results by the newest headlines for updated articles.
        nyt_article_search = req.get(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&sort=newest&page={i}&fq=news_desk:(\"Energy\" \"Environment\" \"Climate\")&api-key={NYT.api_key}")
        
        # Get json data from the API response to parse results
        resp = nyt_article_search.json()

        # Gather and format relevant data from the response body: 
        # Article Headline, URL, Datetime, and Source. 
        for article in resp['response']['docs']:
            article_data = {
                'Headline': article['headline']['main'],
                'URL': article['web_url'],
                'Datetime': article['pub_date'],
                'Source': article['source'],
                }
            # Add each article to the list of articles
            data.append(article_data)

    return data


def get_news(query):
    # Get New York Times results (NewsAPI does not seem to source articles from NYT.)
    nyt_search = nyt_articles(query)
    
    # Query NewsAPI's "everything" endpoint to get articles in English.
    newsapi_search = req.get(f"https://newsapi.org/v2/everything?q={query}&language=en&apiKey={NewsAPI.api_key}")
    
    # Get json data from the API response to parse results
    resp = newsapi_search.json()['articles']
    
    data = []

    # Gather and format relevant data from the response body: 
    # Article Headline, URL, Datetime, and Source. 
    for article in resp:
        article_data = {
            'Headline': article['title'],
            'URL': article['url'],
            'Datetime': article['publishedAt'],
            'Source': article['source']['name'],
            }
        
        # Add each article to the list of articles
        data.append(article_data)

    # Return the master list of articles from both sources (formatted in the same way)
    # in order to display in EnviroHub's news datatable format.
    return nyt_search + data 
