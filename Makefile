up:
	docker compose up db -d && docker compose up -d

setup: up
	docker exec django-crud-web-1 python manage.py migrate

test:
	docker exec django-crud-web-1 python manage.py test
