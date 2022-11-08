import requests
from bs4 import BeautifulSoup
from pprint import pprint
from fake_headers import Headers
from functions import get_preview_list_articles, get_full_list_articles


def main(keywords):
    url = 'https://habr.com/ru/all/'
    header = Headers(
        browser="chrome",
        os="win",
        headers=True
    )
    headers = header.generate()
    response = requests.get(url, headers=headers)
    text = response.text
    soup = BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')
    # # Поиск ключевых слов в preview информации
    # return get_preview_list_articles(keywords, articles)
    # # Поиск ключевых слов во всей статье
    # return get_full_list_articles(keywords, articles)


if __name__ == '__main__':
    KEYWORDS = ['как', 'какsssss']
    pprint(main(KEYWORDS))
