# SheepFish challenge

## Instalation
1. Clone repository:
```
git clone https://github.com/Dima12334/sheepfish.git
```
2. Create python virtual environment:
```
python3 -m venv <venv_name>
source <venv_name>/bin/activate
```
3. Install project dependencies:
```
pip install -r requirements/development.txt
```
4. Complete the config/.env file.
5. Run docker containers (PostgreSQL, Redis, wkhtmltopdf):
```
docker-compose up
```
6. Run migrations:
```
python manage.py migrate
```
7. Create django superuser:
```
python manage.py createsuperuser
```
8. Go to admin panel and create the first record at "Intervals" table, and then create record in the "Periodic Tasks" for the apps.printers.tasks.print_rendered_checks task.
9. Run celery worker, beat and flower:
```
celery --app config.celery.app worker -l info
celery --app config.celery.app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
celery --broker=redis://127.0.0.1:6379/0 flower
```
10. Run server:
```
python manage.py runserver
```
11. Done. Use the App.
