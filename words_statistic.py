import pymorphy2
import re
import collections


def flat(not_flat_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return [item for sublist in not_flat_list for item in sublist]


def parse_nouns_in_titles_articles(titles_articles):
    ''' Выбрать существительные '''

    # Разбиваем заголовок на слова
    # Если не очистить строку от "мусора", могут помешать подсчёту статистики
    # кавычки или ещё какое-нибудь безобразие (для этого используем re)
    words = flat([
        re.sub('[^a-zA-Zа-яА-Я0-9 -]', '', title_article['title']).split()
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
            if ('NOUN' in word_parses[0].tag or
                    'LATN' in word_parses[0].tag):
                # Латинские имена считаем существительными :) статистика с ними
                # интереснее
                nouns.append(word_parses[0].normal_form)
    return nouns


def get_top_words(words, top_size=10):
    ''' Сформировать ТОП слов '''
    return collections.Counter(words).most_common(top_size)
