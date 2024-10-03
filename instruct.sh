Установка и запуск

    Клонируйте репозиторий и перейдите в директорию проекта:

    bash

git clone https://github.com/yourusername/package_builder.git
cd package_builder

Создайте виртуальное окружение и активируйте его:

bash

python -m venv venv
source venv/bin/activate

Установите зависимости:

bash

pip install --upgrade pip
pip install -r requirements.txt

Создайте файл .env на основе примера и заполните необходимые значения.

Примените миграции и создайте суперпользователя:

bash

python manage.py migrate
python manage.py createsuperuser

Запустите Celery воркер:

В отдельном терминале, активируйте виртуальное окружение и выполните:

bash

celery -A package_builder worker --loglevel=info

Запустите сервер разработки:

bash

    python manage.py runserver

    Откройте браузер и перейдите по адресу http://localhost:8000/admin/ для доступа к админ-панели.
