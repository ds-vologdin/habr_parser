# habr_parser
Парсер habr.com. Формирует ТОП самых используемых существительных в заголовках статей.

## Установка
```git clone https://github.com/ds-vologdin/habr_parser.git```

## Использование
```python3 habr_parser.py --pages=50```
получили 50 страниц с habr.com
количество статей: 498

| Начало недели |                       Популярные слова                       |
|:-------------:|--------------------------------------------------------------|
|  2018-04-09   | система (2), знакомство (2), проектирование (2), поддержка (2) , безопасность (2), программирование (2), тест (1) |
|  2018-04-16   | система (10), приложение (8), разработка (8), работа (8), новое (6), апрель (6), помощь (5), часть (5), код (4)  |
|  2018-04-23   | часть (15), система (13), управление (8), разработка (7), помощь (6), решение (6), использование (6), сервер (5)   |


Обратите внимание, что на habr.com доступно для выгрузки только 100 страниц.
