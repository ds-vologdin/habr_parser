import requests
from bs4 import BeautifulSoup
from datetime import timedelta
import asyncio
import dateparser


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


def get_titles_articles_with_raw_habr_pages(habr_pages):
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
