#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def fetch_raw_habr_pages(pages=10):
    ''' Получить сырые данные с хабра '''
    pages_habr = []
    for page_number in range(1, pages+1):
        r = requests.get('https://habr.com/all/page%d/' % page_number)
        pages_habr.append(r.text)
    return pages_habr


def convert_habr_date_to_datetime(date_habr):
    ''' Конвертер строковой даты с habr.com  в datetime '''
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    date_habr = date_habr.replace('сегодня в', today.strftime('%d-%m-%Y'))
    date_habr = date_habr.replace('вчера в', yesterday.strftime('%d-%m-%Y'))
    date_habr = date_habr.replace(' января в', yesterday.strftime('-01-%Y'))
    date_habr = date_habr.replace(' февраля в', yesterday.strftime('-02-%Y'))
    date_habr = date_habr.replace(' марта в', yesterday.strftime('-03-%Y'))
    date_habr = date_habr.replace(' апреля в', yesterday.strftime('-04-%Y'))
    date_habr = date_habr.replace(' мая в', yesterday.strftime('-05-%Y'))
    date_habr = date_habr.replace(' июня в', yesterday.strftime('-06-%Y'))
    date_habr = date_habr.replace(' июля в', yesterday.strftime('-07-%Y'))
    date_habr = date_habr.replace(' августа в', yesterday.strftime('-08-%Y'))
    date_habr = date_habr.replace(' сентября в', yesterday.strftime('-09-%Y'))
    date_habr = date_habr.replace(' октября в', yesterday.strftime('-10-%Y'))
    date_habr = date_habr.replace(' ноября в', yesterday.strftime('-11-%Y'))
    date_habr = date_habr.replace(' декабря в', yesterday.strftime('-12-%Y'))
    return datetime.strptime(date_habr, '%d-%m-%Y %H:%M')


def parse_habr_pages(habr_pages):
    ''' Распарсить сырые страницы: выбрать заголовки статетей с датами
        публикации '''
    headers_articles = []
    for page_text in habr_pages:
        soup = BeautifulSoup(page_text, "html.parser")
        articles = soup.find_all("article", class_="post")

        for article in articles:
            print('-'*80)

            date_of_publication_tag = article.find("span", class_="post__time")
            if not date_of_publication_tag:
                continue

            date_of_publication = convert_habr_date_to_datetime(
                date_of_publication_tag.get_text()
            )
            print(date_of_publication)

            header_article_tag = article.find("a", class_="post__title_link")
            if not header_article_tag:
                continue

            header_article = header_article_tag.get_text()

            print(header_article)
            headers_articles.append(
                {'date': date_of_publication,
                 'header': header_article}
            )

    return []


def divide_headers_at_weeks(headers_articles):
    ''' Разделить заголовки по неделям '''
    return []


def parse_nons_in_headers_articles(headers_articles):
    ''' Выбрать существительные '''
    return []


def get_top_words(nons, top_size=10):
    ''' Сформировать ТОП слов '''
    return []


def main(args):
    habr_pages = fetch_raw_habr_pages(pages=10)
    headers_articles = parse_habr_pages(habr_pages)
    headers_articles_weeks = divide_headers_at_weeks(headers_articles)
    for headers_articles in headers_articles_weeks:
        nons = parse_nons_in_headers_articles(headers_articles)
        nons_top = get_top_words(nons, top_size=10)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
