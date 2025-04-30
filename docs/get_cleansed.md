### Старт с cleansed

Весь ЕTL в `etl/cleansed_entrypoint`, но запуск из бэкапа.

1. Нужные креды в энве
2. `docker-compose up -d`
3. `docker cp cleansed.backup music_postgres:/db/cleansed.backup`
4. Создается только cleansed `docker exec -e PGPASSWORD={your_pass} {your_container} pg_restore -U {your_user} -d {your_db} -n cleansed -Fc /db/cleansed.backup` 
