import pymorphy2
import re
import collections


def flat(not_flat_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return [item for sublist in not_flat_list for item in sublist]


def parse_nouns_in_titles_articles(titles_articles, morph=None):
    ''' Выбрать существительные.
    В случае использования функции в цикле для оптимизации работы имеет смысл
    задать аргумент morph:
    morph = pymorphy2.MorphAnalyzer()
    for titles_articles in titles_articles_weeks:
        parse_nouns_in_titles_articles(titles_articles, morph)
    '''

    # Разбиваем заголовок на слова
    # Если не очистить строку от "мусора", могут помешать подсчёту статистики
    # кавычки или ещё какое-нибудь безобразие (для этого используем re)
    words = flat([
        re.sub('[^a-zA-Zа-яА-Я0-9 -]', '', title_article['title']).split()
        for title_article in titles_articles['titles_articles']
    ])

    if not morph:
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
            if ('NOUN' in word_parses[0].tag or
                    'LATN' in word_parses[0].tag):
                # Латинские имена считаем существительными :) статистика с ними
                # интереснее
                nouns.append(word_parses[0].normal_form)
    return nouns


def parse_nouns_in_titles_articles_at_weeks(titles_articles_weeks, top_size):
    top_nouns_weeks = []
    morph = pymorphy2.MorphAnalyzer()
    for titles_articles in titles_articles_weeks:
        # за пределами цикла задаём morph в целях оптимизации:
        # нехорошо много-много раз загружать одни и те же словари pymorphy2
        nouns = parse_nouns_in_titles_articles(titles_articles, morph)
        top_nouns_weeks.append({
            'date': titles_articles['date'],
            'top_words': get_top_words(nouns, top_size),
        })
    return top_nouns_weeks


def get_top_words(words, top_size=10):
    ''' Сформировать ТОП слов '''
    return collections.Counter(words).most_common(top_size)
