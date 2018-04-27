#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


def fetch_raw_habr_pages(pages=10):
    ''' Получить сырые данные с хабра '''
    pages_habr = []
    for page_number in range(1, pages+1):
        r = requests.get('https://habr.com/all/page%d/' % page_number)
        pages_habr.append(r.text)
    return pages_habr


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
            date_of_publication = date_of_publication_tag.get_text() \
                if date_of_publication_tag else ''
            print(date_of_publication)
            
            header_article_tag = article.find("a", class_="post__title_link")
            header_article = header_article_tag.get_text() \
                if header_article_tag else ''
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
