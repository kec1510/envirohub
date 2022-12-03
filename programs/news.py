from bs4 import BeautifulSoup
import requests as req

import datetime as dt
from datetime import datetime, date
from programs.keys import NYT, NewsAPI

today = date.today().strftime("%Y%m%d")

lweek = (date.today() - dt.timedelta(weeks=1)).strftime("%Y%m%d")

def nyt_articles(query):
    data = []
    for i in range(3):
        nyt_article_search = req.get(f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&sort=newest&page={i}&fq=news_desk:(\"Energy\" \"Environment\" \"Climate\")&api-key={NYT.api_key}")
        resp = nyt_article_search.json()
        for article in resp['response']['docs']:
            article_data = {
                'Headline': article['headline']['main'],
                'URL': article['web_url'],
                'Datetime': article['pub_date'],
                'Source': article['source'],
                }
            data.append(article_data)

    return data

# nyt_articles('climate change')
def get_news(query):
    nyt_search = nyt_articles(query)
    newsapi_search = req.get(f"https://newsapi.org/v2/everything?q={query}&language=en&apiKey={NewsAPI.api_key}")
    resp = newsapi_search.json()['articles']
    
    data = []
    for article in resp:
        article_data = {
            'Headline': article['title'],
            'URL': article['url'],
            'Datetime': article['publishedAt'],
            'Source': article['source']['name'],
            }
        data.append(article_data)

    return nyt_search + data
