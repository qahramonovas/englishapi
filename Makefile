create_app:
	python3 manage.py startapp apps

create_user:
	python3 manage.py createsuperuser admin


mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

run:
	python3 manage.py runserver localhost:8000