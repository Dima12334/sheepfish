# SheepFish challenge

## Installation
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
8. Run celery worker, celery beat and flower:
```
celery --app config.celery.app worker -l info
celery --app config.celery.app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
celery --broker=redis://localhost:6379/0 flower
```
9. Run server:
```
python manage.py runserver
```
10. Go to the admin panel and create the first record at `Intervals` table, and then create record in the `Periodic Tasks` for the `apps.printers.tasks.print_rendered_checks` task (set this task as a `Task (custom)`) with `Schedule -> Interval Schedule` what you created.
On the `Periodic Tasks` page you can also specify the printers on which you want to print the check (By default, all existing printers will be specified). To do this, you need to add `{"printer_pks": [1, 2]}` to `Arguments` -> `Keyword Arguments`, where [1, 2] is an example of a list of `Printer` model IDs.
11. Done. Use the App.
