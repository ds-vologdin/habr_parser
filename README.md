# habr_parser
Парсер habr.com. Формирует ТОП самых используемых существительных в заголовках статей.
К существительным здесь мы приравниваем и все слова на латинице (с ними статистика смотрится интереснее).

## Установка
Пока доступна установка только с github.com

```git clone https://github.com/ds-vologdin/habr_parser.git```

## Использование

Для получения ТОП самых используемых слов используйте приложение habr_top_nouns.py

```
python habr_top_nouns.py --pages 20
получили 20 страниц с habr.com
количество статей: 199
+---------------+--------------------------------------------------------------+
| Начало недели |                       Популярные слова                       |
+===============+==============================================================+
|               | java (4), обработка (3), раз (3), тестирование (2), ошибка   |
|  2018-05-14   | (2), api (2), c (2), число (2), часть (2), обзор (2), блок   |
|               | (2), код (2), итог (2), май (2), the (2), перевод (2), dev   |
|               | (1), ipv4 (1), 3cx (1), противостояние (1)                   |
+---------------+--------------------------------------------------------------+
|               | разработка (6), пример (6), игра (6), часть (6),             |
|               | использование (6), пользователь (5), google (5), помощь (5), |
|  2018-05-21   | работа (4), сеть (4), задача (4), программирование (4), опыт |
|               | (4), компания (4), настройка (3), gdpr (3), марвин (3),      |
|               | обучение (3), миллиард (3), платформа (3)                    |
+---------------+--------------------------------------------------------------+

```
### Параметры habr_top_nouns.py
```
--pages PAGES        Количество страниц с habr.com. По-умолчанию 20. 
--top-size TOP_SIZE  Количество слов за каждую неделю. По-умолчанию 20. 
```
Обратите внимание, что на habr.com доступно для выгрузки только 100 страниц.
