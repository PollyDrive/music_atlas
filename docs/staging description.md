## Запуск с 0
### staging_entrypoint.py

Что в нём происходит:
#### load_country.main()
Загружает страны через Ninja API на основе iso-кодов.
Сохраняет их в таблицу staging.country.

#### load_lastfm_top_artists.main()
Загружает топ-исполнителей по странам с Last.fm.
Сохраняет чарты в staging.artist_charts.

#### load_artist_info.main()
Загружает расширенную информацию об исполнителях с Last.fm.
Сохраняет в staging.artist_info.

#### load_artist_tags_from_lastfm.main()
Загружает жанры/теги артистов с Last.fm.
Сохраняет в staging.artist_tags.

#### load_artist_musicbrainz.main()
Обогащает информацию об артистах через базу MusicBrainz.
Добавляет правильные MBID и другую допинформацию.

#### patch_artist_mbid.main()
Патчит артистов, у которых неправильно проставлены MBID или их нет.

#### load_alcohol_consumption.main()
Загружает данные о потреблении алкоголя по странам

#### load_country_languages.main()
Загружает информацию о языках стран

#### load_depression_rate.main()
Загружает уровень депрессии по странам из готового csv в data

#### load_press_freedom.main()
Загружает индекс свободы прессы по странам из готового csv в data

#### load_suicide_rate.main()
Загружает уровень суицидов по странам.

#### pre_cleanup_artists.main()
Делает предварительную чистку данных об артистах: исправляет имена, убирает мусор.