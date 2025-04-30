Music Atlas is a platform for wacky correlations that shows various weird connections between the popularity of artists or genres and various country metrics.
For example:
- Comparing the number of k-pop concerts and the suicide rate.
- What exactly does a "sex playlist" mean in different countries?
- Comparing the birth rate and the popularity of new metal bands in the early 2000s.
- The influence of the economic system on the popularity of the chanson genre.
- The relationship between the divorce rate and the popularity of breakup songs

In the future, we plan to:
- Collect song data (metadata + lyrics) from various open music databases.
- Research connections (song ↔ author ↔ genre ↔ country ↔ year).
- Correlations and statistics on graphs by year.


Music Atlas — это платформа для дурацких корреляций, которая показывает странные связи между различными показателями страны и популярными в ней исполнителями.

В будущем планируется:
- сбор данных о песнях (метаданные + тексты) из различных открытых баз данных музыки.
- исследование связей (песня ↔ автор ↔ жанр ↔ страна ↔ год).
- корреляции и статистика на графиках по годам.

## Стек
PostgreSQL, 
Docker, 
Python ≥ 3.10, 
pandas, 
SQLAlchemy, 
psycopg2, 
Alembic 


## Запуск проекта c 0 для staging
    docs/init.md
## Инициализация cо слоя Cleansed
    docs/get_cleansed.md

Что я хотела:
- Сравнение количества концертов k-pop и уровня самоубийств.
- Что именно означает «секс-плейлист» в разных странах?
- Сравнение уровня рождаемости и популярности новых метал-групп в начале нулевых.
- Влияние экономической системы на популярность жанра «шансон».
- Связь между количеством разводов и популярностью песен о расставаниях

Что я получила:
- В странах, с высоким показателем A и B, чаще слушают исполнителей X, Y, Z
- Чем выше/ниже показатель С в стране, тем реже/чаще в топе исполнители X, Y, Z