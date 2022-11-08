import datetime
import re
from fake_headers import Headers
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


# Получение заголовка статьи
def get_heading(publication):
    heading = publication.find(class_="tm-article-snippet__title tm-article-snippet__title_h2")
    heading = heading.text
    return heading


# Получение хабов/хештегов статьи
def get_hubs(publication):
    hubs = publication.find_all(class_="tm-article-snippet__hubs")
    hubs_str = ''
    for hub in hubs:
        hubs_str += ' ' + hub.text
    return hubs_str


# Получение preview-информации
def get_preview_information(publication):
    preview_information = publication.find(
        class_="article-formatted-body article-formatted-body article-formatted-body_version-1")
    if preview_information:
        return preview_information.text
    else:
        preview_information = publication.find(
            class_="article-formatted-body article-formatted-body article-formatted-body_version-2")
        return preview_information.text


# Получение полного текста статьи
def full_information(url):
    header = Headers(
        browser="chrome",
        os="win",
        headers=True
    )
    headers = header.generate()
    response = requests.get(url, headers=headers)
    text = response.text
    soup = BeautifulSoup(text, features='html.parser')
    preview_information = soup.find(
        class_="article-formatted-body article-formatted-body article-formatted-body_version-1")
    if preview_information:
        return preview_information.text
    else:
        preview_information = soup.find(
            class_="article-formatted-body article-formatted-body article-formatted-body_version-2")
        return preview_information.text


# Замена символов в тексте и преобразование в список
def text_change(text):
    pattern = r'\W'
    replacement = r' '
    text = re.sub(pattern, replacement, text)
    preview_list = text.lower().split()
    return preview_list


# Получение даты статьи
def get_date(publication):
    date = publication.find(class_="tm-article-snippet__datetime-published")
    date = date.time.get('datetime')
    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    date = date.strftime("%d %b %Y %H:%M")
    return date


# Получение ссылки на статью
def get_link(publication):
    href = publication.find(class_="tm-article-snippet__title-link")
    href = href.get('href')
    url = 'https://habr.com'
    link = url + href
    return link


# Проверка статей на ключевые слова
def checking_for_keywords(keywords, preview_list, necessary_articles, publication):
    for word in keywords:
        if word in preview_list:
            list_ = [get_date(publication), get_heading(publication), get_link(publication)]
            return necessary_articles.append(list_)


# Получение списка подходящих статей из preview информации
def get_preview_list_articles(keywords, articles):
    necessary_articles = []
    for article in articles:
        preview_str = ''
        preview_str += ' ' + get_heading(article)
        preview_str += ' ' + get_hubs(article)
        preview_str += ' ' + get_preview_information(article)
        preview_list = text_change(preview_str)
        checking_for_keywords(keywords, preview_list, necessary_articles, article)
    if necessary_articles:
        return [necessary_articles, f'Найдено {len(necessary_articles)} статей']
    else:
        return 'Совпадений не найдено'

# Получение списка подходящих статей из всей информации
def get_full_list_articles(keywords, articles):
    necessary_articles = []
    for article in tqdm(articles, desc='Обработка статей'):
        preview_str = ''
        preview_str += ' ' + get_heading(article)
        preview_str += ' ' + get_hubs(article)
        preview_str += ' ' + full_information(get_link(article))
        preview_list = text_change(preview_str)
        checking_for_keywords(keywords, preview_list, necessary_articles, article)
    if necessary_articles:
        return [necessary_articles, f'Найдено {len(necessary_articles)} статей']
    else:
        return 'Совпадений не найдено'
