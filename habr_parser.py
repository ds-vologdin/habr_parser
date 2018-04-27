#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def fetch_raw_habr_pages(pages=20):
    ''' Получить сырые данные с хабра '''
    return []


def parse_habr_pages(raw_habr_pages):
    ''' Распарсить сырые страницы: выбрать заголовки статетей с датами
        публикации '''
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
    raw_habr_pages = fetch_raw_habr_pages(pages=20)
    headers_articles = parse_habr_pages(raw_habr_pages)
    headers_articles_weeks = divide_headers_at_weeks(headers_articles)
    for headers_articles in headers_articles_weeks:
        nons = parse_nons_in_headers_articles(headers_articles)
        nons_top = get_top_words(nons, top_size=10)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
