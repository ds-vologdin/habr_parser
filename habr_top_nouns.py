#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from texttable import Texttable
import argparse

from words_statistic import parse_nouns_in_titles_articles, get_top_words
from habr_parse import (
    fetch_raw_habr_pages, parse_habr_pages, divide_titles_at_weeks
)


def parse_argv():
    description_programm = '''Приложение для подсчёта наиболее употребимых \
существительных в заголовках статей на habr.com'''
    parser = argparse.ArgumentParser(description=description_programm)
    parser.add_argument(
        "--pages", type=int, default=20,
        help="Количество страниц с habr.com. По-умолчанию 20."
    )
    parser.add_argument(
        "--top-size", type=int, default=20,
        help="Количество слов за каждую неделю. По-умолчанию 20."
    )
    return parser.parse_args()


def output_words_stat(nouns_weeks):
    # Инициализируем таблицу на печать
    table = Texttable()
    table.set_cols_align(['c', 'l'])
    table.set_cols_valign(['m', 'm'])
    table.header(['Начало недели', 'Популярные слова'])
    for nouns_week in nouns_weeks:
        top_words = nouns_week['top_words']
        table.add_row((
            nouns_week['date'],
            ', '.join(['%s (%d)' % (noun, count) for noun, count in top_words])
        ))
    # Прорисовываем таблицу
    print(table.draw())


def main(args):

    # Парсим argv
    args = parse_argv()

    pages_count = args.pages
    top_size = args.top_size

    # Получаем содержимое страниц
    habr_pages = fetch_raw_habr_pages(pages_count)
    print('получили {0} страниц с habr.com'.format(len(habr_pages)))

    # Получаем список заголовков
    titles_articles = parse_habr_pages(habr_pages)
    print('количество статей: {0}'.format(len(titles_articles)))

    # Разбиваем выборку на недели
    titles_articles_weeks = divide_titles_at_weeks(titles_articles)

    # Формируем список популярных существительных по каждой неделе
    top_nouns_weeks = []
    for titles_articles in titles_articles_weeks:
        nouns = parse_nouns_in_titles_articles(titles_articles)
        top_nouns_weeks.append({
            'date': titles_articles['date'],
            'top_words': get_top_words(nouns, top_size),
        })
    output_words_stat(top_nouns_weeks)
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
