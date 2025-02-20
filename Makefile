create_app:
	python3 manage.py startapp apps

create_user:
	python3 manage.py createsuperuser


mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

migration_create:
	mkdir apps/migrations
	touch appp/migrations/__init__.py