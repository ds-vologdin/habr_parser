import sys
from texttable import Texttable
import argparse

from words_statistic import parse_nouns_in_titles_articles_at_weeks
from habr_parse import fetch_raw_habr_pages, divide_titles_at_weeks
from habr_parse import get_titles_articles_with_raw_habr_pages


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
    args = parse_argv()

    pages_count = args.pages
    top_size = args.top_size

    habr_pages = fetch_raw_habr_pages(pages_count)
    print('получили {0} страниц с habr.com'.format(len(habr_pages)))

    titles_articles = get_titles_articles_with_raw_habr_pages(habr_pages)
    print('количество статей: {0}'.format(len(titles_articles)))

    titles_articles_weeks = divide_titles_at_weeks(titles_articles)

    top_nouns_weeks = parse_nouns_in_titles_articles_at_weeks(
        titles_articles_weeks, top_size
    )

    output_words_stat(top_nouns_weeks)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
