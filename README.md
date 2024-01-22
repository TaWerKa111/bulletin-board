# Сервис по размещению объявлений

# Стек
- Python 3.11
- FastAPI
- PostgreSQL 14
- Docker

# Переменные окружения
- DATABASE_URL: str - url для подключения к базе данных. 
По умолчанию: postgresql+asyncpg://admin:admin@db/bulletin-app

# Команды проекта

# Команды

##  Для запуска
```shell
docker-compose -it -f docker-compose.local.yaml up --build
```

## Для остановки
```shell
docker-compose down
```
