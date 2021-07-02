# Кошелёк
## Web-приложение для учета финансов
[Здесь можно посмотреть приложение вживую](https://financeapp2021.pythonanywhere.com/finance/main/)
- [Техническое задание](https://docs.google.com/document/d/1dkKmHNVEv3XTtc6rZiyJrquisvWJdmO1o7JKO_b9_ik/)
- [Тест план](https://docs.google.com/document/d/1uujbqGMMhEJnsvm4cqkhcyzun9L5D462myncgFV3TsM/)
- [Чек лист](https://docs.google.com/spreadsheets/d/1G-8lHKCwYIZhkXT9PRRuy_p3V3uLeQa1MUd_bRwTdGM/)
- [Отчет о тестировании](https://docs.google.com/document/d/14XyGG1qOv1P9lXa-AyVrYmBnpTed6DN9aFHdSKjMEvE/)
- [Приложение к отчету о тестировании](https://docs.google.com/document/d/1lrDWGvBjzV41e0JsdDUpoELavagpmItEo15sChCqtzA/)

## Основные возможности:
- Возможность добавления, удаления, редактирования записей пользователем о доходах и расходов
- Возможность выбора и добавления новых категорий доходов и расходов
- Возможность просмотра статистики доходов и расходов
- История транзакций с фильтрацией по различным параметрам


## Установка и запуск
### С помощью Docker
Сборка и первоначальный запуск
```sh
docker-compose up --build
```

Запуск тестов (пока не написаны)
```sh
docker-compose exec web python django_app/manage.py test
```

Для создания суперпользователя
```sh
docker-compose exec web python django_app/manage.py createsuperuser
```

После запуска докера сайт будет доступен по адресу `http://127.0.0.1:8080/`


### Без использования Docker
Создаем виртуальное окружение
```sh
python3 -m venv .env
```

Активируем виртуальное окружение
```sh
source .env/bin/activate
```

Устанавливаем зависимости
```sh
pip install -r requirements.txt
```

Миграции БД
```sh
python django_app/manage.py migrate
```

Локализация
```sh
django-admin compilemessages
```

Загрузка фикстур (чтобы было на что посмотреть в приложении)
```sh
python django_app/manage.py loaddata fixtures.json
```

Запуск dev-сервера
```sh
python django_app/manage.py runserver 8080
```

## TODO
- Написать тесты
- Создание нескольких счетов
- Планирование
- Создание групп для "совместных бюджетов" и система инвайтов для них
- Напоминания о предстоящих платежах
- "Боевой" конфиг