# Set up the project for local development

> Prerequisites: python3 and pip

```bash
docker-compose build
docker-compose run web pip install -r requirements.txt
docker-compose run web python manage.py migrate
docker-compose up web
```
