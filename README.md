# Продуктивизация ML сервисов

Этот репозиторий содержит весь необходимый код для моих заметок про хорошие практики продуктивизации ML решений. Главная задача этих заметок - показать как сделать из вашей ML модельки качественное решение, которое можно использовать в продакшене.

Заметки можно прочитать в блоге: https://mvrck.space/

Всего есть пять заметок:
1. [Мотивация для использования практик ](https://mvrck.space/posts/ml-best-practices-p1-motivation/)
2. [Контроль качества кода](https://mvrck.space/posts/ml-best-practices-p2-code-quality/)
3. [Разработка сервисной части](https://mvrck.space/posts/ml-best-practices-p3-service/)
4. [Наблюдаемость сервиса](https://mvrck.space/posts/ml-best-practices-p4-observability/)
5. [Контейнеризация сервиса](https://mvrck.space/posts/ml-best-practices-p5-containers/)

## Общая информация

Главная часть кода это сервис, который реализует простую ML логику. Вместе с логикой в сервисе есть все необходимое для качественной продуктовой эксплуатации и поддержки.

Есть логирование, трейсинг, сервсные метрики. Настройка происходит через переменные окружения. Контейнеризация с использование `Docker` и `docker-compose` для удобного запуска не только сервиса но и инфраструктуры (`Jaeger` и `Prometheus`).

## Техстек

- Сервис -- `FastApi`
- Трейсинг -- `Opentelemetry + Jaeger`
- Логи -- `Loguru`
- Метрики -- `Prometheus`
- Валидация данных -- `Pydantic`
- Контейнеризация -- `Docker + docker-compose`
- Качество кода -- `pre-commiter`
- Тесты -- `pytest`

## Как пользоваться

Для запуска контейнера с сервисом и всей инфраструктурой:
1. `git clone <repo address>`
2. `cd ml-service-in-production`
3. `docker-compose up --build` -- запуск контейнера
4. Адреса:
    - Сервис -- http://localhost:8000/docs
    - Prometheus -- http://localhost:9090/
    - Jaeger -- http://localhost:16686/

Для локального запуска сервиса без инфраструктуры:
1. `git clone <repo address>`
2. `cd ml-service-in-production`
3. `python3 -m venv venv` -- подготовка виртуального окружения
4. `source venv/bin/activate` -- активация окружения
5. `pip install -r requirements.txt` -- установка зависимостей
6. `uvicorn main:app` -- запуск сервиса

Для запуска тестов:
1. Все пункты для локального запсука сервиса
2. `pip install pytest` -- установка пакета для тестирования
3. `pytest -vv` -- для просмотра результатов

## Документация

Очень подробно про каждую часть кода я писал в [блоге](https://mvrck.space/) там можно прочитать для чего нужна каждая технология и как именно реализовано её применение в рамках сервиса.
