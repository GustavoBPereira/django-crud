up:
	docker compose up

test:
	docker exec django-crud-web-1 python manage.py test
