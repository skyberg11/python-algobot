import requests as rq
from lib.struct import *
from bs4 import BeautifulSoup as bs
import pandas as pd

def query_list(word : str):
    q = []
    url = "https://stackoverflow.com/search?tab=votes&q=" + word
    request = rq.get(url)
    soup = bs(request.text, "html.parser")
    lists = soup.find_all('div', class_='js-search-results')
    votes = soup.find_all('span', class_="vote-count-post")
    if(len(lists) == 0):
        return q
    search_results = lists[0].find_all('div', class_='search-result')
    for result, vote_count in zip(search_results, votes):
        # show = result.find_all('div', class_="excerpt") 
        # Search preview but we dont need it, do we?
        q.append(query(result.a['title'], "https://stackoverflow.com" + result.a['href'], "", int(vote_count.text)))
    return q

