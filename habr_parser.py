#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import asyncio
import pymorphy2
import collections
from texttable import Texttable
import getopt


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
                'https://habr.com/all/page%d/' % page_number
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
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    date_habr = date_habr.replace('сегодня в', today.strftime('%d-%m-%Y'))
    date_habr = date_habr.replace('вчера в', yesterday.strftime('%d-%m-%Y'))
    date_habr = date_habr.replace(' января в', today.strftime('-01-%Y'))
    date_habr = date_habr.replace(' февраля в', today.strftime('-02-%Y'))
    date_habr = date_habr.replace(' марта в', today.strftime('-03-%Y'))
    date_habr = date_habr.replace(' апреля в', today.strftime('-04-%Y'))
    date_habr = date_habr.replace(' мая в', today.strftime('-05-%Y'))
    date_habr = date_habr.replace(' июня в', today.strftime('-06-%Y'))
    date_habr = date_habr.replace(' июля в', today.strftime('-07-%Y'))
    date_habr = date_habr.replace(' августа в', today.strftime('-08-%Y'))
    date_habr = date_habr.replace(' сентября в', today.strftime('-09-%Y'))
    date_habr = date_habr.replace(' октября в', today.strftime('-10-%Y'))
    date_habr = date_habr.replace(' ноября в', today.strftime('-11-%Y'))
    date_habr = date_habr.replace(' декабря в', today.strftime('-12-%Y'))
    return datetime.strptime(date_habr, '%d-%m-%Y %H:%M')


def parse_habr_pages(habr_pages):
    ''' Распарсить сырые страницы: выбрать заголовки статей с датами
        публикации '''
    headers_articles = []
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
            header_article_tag = article.find("a", class_="post__title_link")
            if not header_article_tag:
                continue

            header_article = header_article_tag.get_text()

            headers_articles.append(
                {'date': date_of_publication,
                 'header': header_article}
            )
    return headers_articles


def get_weeks(date_begin, date_end):
    # Формируем список недель
    data_cur = date_begin - timedelta(days=date_begin.weekday())
    delta = date_end - data_cur
    return [
        (data_cur + timedelta(days=i), data_cur + timedelta(days=i+7))
        for i in range(0, delta.days, 7)
    ]


def divide_headers_at_weeks(headers_articles):
    ''' Разделить заголовки по неделям '''
    if not headers_articles:
        return []
    # Берём даты публикаций самой старой и самой свежей статьи
    date_begin = headers_articles[-1]['date'].date()
    date_end = headers_articles[0]['date'].date()

    # Формируем список недель
    weeks = get_weeks(date_begin, date_end)

    # Разбиваем статьи по неделям
    headers_articles_weeks = []
    for date_begin_week, date_end_week in weeks:
        headers_articles_weeks.append({
            'date': date_begin_week,
            'headers_articles': [
                header_article for header_article in headers_articles
                if (header_article['date'].date() >= date_begin_week and
                    header_article['date'].date() < date_end_week)
            ]
        })
    return headers_articles_weeks


def parse_nouns_in_headers_articles(headers_articles):
    ''' Выбрать существительные '''
    # Разбиваем заголовок на слова
    words = flat([
        header_article['header'].split()
        for header_article in headers_articles['headers_articles']
    ])

    morph = pymorphy2.MorphAnalyzer()
    nouns = []
    for word in words:
        # Морфологический разбор
        word_parses = morph.parse(word)
        # Выбирать из всех морфологических значений не верно - много мусора
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


def usage():
    print("usage: python3", sys.argv[0], "OPTIONS")
    print("OPTIONS")
    help_text = '''--pages=XX По умолчанию pages=20
--help
'''
    print(help_text)


def parse_argv():
    # Смотрим переданные параметры и инициируем переменные
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], '', ['pages=', 'help'])
    except getopt.GetoptError as err:
        print("ошибка задания параметров: ", err)
        usage()
        return None

    options = {}
    for o, a in opts:
        if o == '--pages':
            try:
                options['pages'] = int(a)
            except:
                print('pages должен быть числом')
                usage()
                return None
        elif o == '--help':
            usage()
            return None
        else:
            print('неверный параметр: %s' % (o))
            usage()
            return None
    return options


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
    options = parse_argv()

    pages_count = options.get('pages', 20)

    # Получаем содержимое страниц
    habr_pages = fetch_raw_habr_pages(pages_count)
    print('получили %d страниц с habr.com' % len(habr_pages))

    # Получаем список заголовков
    headers_articles = parse_habr_pages(habr_pages)
    print('количество статей: %d' % len(headers_articles))

    # Разбиваем выборку на недели
    headers_articles_weeks = divide_headers_at_weeks(headers_articles)

    # Формируем список популярных существительных по каждой неделе
    nouns_weeks = []
    for headers_articles in headers_articles_weeks:
        nouns = parse_nouns_in_headers_articles(headers_articles)
        nouns_weeks.append({
            'date': headers_articles['date'],
            'top_words': get_top_words(nouns, top_size=10),
        })
    output_words_stat(nouns_weeks)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
