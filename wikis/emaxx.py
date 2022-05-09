import urllib
import data.settings as urls
from lib.struct import *
from requests_html import HTML
from requests_html import HTMLSession


def handle_response(response):
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"
    results = response.html.find(css_identifier_result)
    q = []
    max_queries = 10
    for result in results:
        max_queries -= 1
        if(max_queries < 0):
            break
        q.append(query(result.find(css_identifier_title, first=True).text,
                    result.find(css_identifier_link, first=True).attrs['href'],
                    result.find(css_identifier_text, first=True).text))
    return q


def query_list(word : str):
    query = urllib.parse.quote_plus(word)
    session = HTMLSession()
    response = session.get(urls.EMAXX_URL + query)
    q = handle_response(response)
    return q

