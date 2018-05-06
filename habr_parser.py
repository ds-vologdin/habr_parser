#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import asyncio
import pymorphy2
import collections
from texttable import Texttable
import argparse
import dateparser


def flat(not_flat_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return [item for sublist in not_flat_list for item in sublist]


async def fetch_raw_habr_pages_async(pages=10):
    ''' Функция асинхронного получения страниц с хабра '''
    loop = asyncio.get_event_loop()
    pages_habr = []
    futures = []
    for page_number in range(1, pages+1):
        futures.append(
            loop.run_in_executor(
                None, requests.get,
                'https://habr.com/all/page{0}/'.format(page_number)
            )
        )
    # Собираем данные в pages_habr
    for future in futures:
        response = await future
        pages_habr.append(response.text)
    return pages_habr


def fetch_raw_habr_pages(pages=10):
    ''' Получить сырые данные с хабра '''
    loop = asyncio.get_event_loop()
    pages_habr = loop.run_until_complete(fetch_raw_habr_pages_async(pages))
    return pages_habr


def convert_habr_date_to_datetime(date_habr):
    ''' Конвертер строковой даты с habr.com  в datetime '''
    return dateparser.parse(date_habr)


def parse_habr_pages(habr_pages):
    ''' Распарсить сырые страницы: выбрать заголовки статей с датами
        публикации '''
    titles_articles = []
    for page_text in habr_pages:
        soup = BeautifulSoup(page_text, "html.parser")
        # Ищем теги article с классом post - вот оно! статьи здесь
        articles = soup.find_all("article", class_="post")

        for article in articles:
            # Ищем тег span с классом post__time - тут дата публикации
            date_of_publication_tag = article.find("span", class_="post__time")
            if not date_of_publication_tag:
                continue
            # Конвертируем её в datetime
            date_of_publication = convert_habr_date_to_datetime(
                date_of_publication_tag.get_text()
            )
            # Ищем тег a с классом post__title_link - тут заголовок статьи
            title_article_tag = article.find("a", class_="post__title_link")
            if not title_article_tag:
                continue

            title_article = title_article_tag.get_text()

            titles_articles.append(
                {'date': date_of_publication,
                 'title': title_article}
            )
    return titles_articles


def get_weeks(date_begin, date_end):
    # Формируем список недель
    data_cur = date_begin - timedelta(days=date_begin.weekday())
    delta = date_end - data_cur
    return [
        (data_cur + timedelta(days=i), data_cur + timedelta(days=i+7))
        for i in range(0, delta.days, 7)
    ]


def divide_titles_at_weeks(titles_articles):
    ''' Разделить заголовки по неделям '''
    if not titles_articles:
        return []
    # Берём даты публикаций самой старой и самой свежей статьи
    date_begin = titles_articles[-1]['date'].date()
    date_end = titles_articles[0]['date'].date()

    # Формируем список недель
    weeks = get_weeks(date_begin, date_end)

    # Разбиваем статьи по неделям
    titles_articles_weeks = []
    for date_begin_week, date_end_week in weeks:
        titles_articles_weeks.append({
            'date': date_begin_week,
            'titles_articles': [
                title_article for title_article in titles_articles
                if (title_article['date'].date() >= date_begin_week and
                    title_article['date'].date() < date_end_week)
            ]
        })
    return titles_articles_weeks


def parse_nouns_in_titles_articles(titles_articles):
    ''' Выбрать существительные '''
    # Разбиваем заголовок на слова
    words = flat([
        title_article['title'].split()
        for title_article in titles_articles['titles_articles']
    ])

    morph = pymorphy2.MorphAnalyzer()
    nouns = []
    for word in words:
        # Морфологический разбор
        word_parses = morph.parse(word)
        # Выбирать из всех морфологических значений неверно - много мусора
        # Например "под", "a", "ли" ...
        # noun_normal_form = ''
        # for word_parse in word_parses:
        #     if 'NOUN' in word_parse.tag:
        #         noun_normal_form = word_parse.normal_form
        #         break
        # Поэтому смотрим первое морфологическое значение - часто употребимое
        if word_parses:
            if 'NOUN' in word_parses[0].tag:
                nouns.append(word_parses[0].normal_form)
    return nouns


def get_top_words(nons, top_size=10):
    ''' Сформировать ТОП слов '''
    return collections.Counter(nons).most_common(top_size)


def parse_argv():
    description_programm = '''Приложение для подсчёта наиболее употребимых \
существительных в заголовках статей на habr.com'''
    parser = argparse.ArgumentParser(description=description_programm)
    parser.add_argument(
        "--pages", type=int, default=20,
        help="Количество страниц с habr.com. Поумолчанию 20."
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
            'top_words': get_top_words(nouns, top_size=10),
        })
    output_words_stat(top_nouns_weeks)
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
