import requests as rq
import data.settings as urls
from lib.struct import *
from bs4 import BeautifulSoup as bs


def query_list(word : str):
    q = []
    url = urls.NEERC_URL + word
    request = rq.get(url)
    soup = bs(request.text, "html.parser")
    lists = soup.find_all('ul', class_='mw-search-results')
    if not lists:
        return q
    search_results = lists[0].find_all('div', class_='mw-search-result-heading')
    for result in search_results:
        prev = rq.get("http://neerc.ifmo.ru" + result.a['href'])
        chunk = bs(prev.text, "html.parser")
        show = chunk.find_all('p')
        q.append(query(result.a['title'], "http://neerc.ifmo.ru" + result.a['href'], str(show[0].text)))
    return q

