# Dokumentacja

## Wymagania

- Python 3.12 
- Django 5.06
- Django REST Framework 3.15
- PostgreSQL 16


# Uruchomienie

## Sklonuj repozytorium

```git clone https://github.com/SkynetV5/mga_zadanie.git```

## Utwórz i aktywuj wirtualne środowisko

Na systemie Unix/MacOS
```python3 -m venv venv```
```source venv/bin/activate```

Na systemie Windows
```python -m venv venv```
```venv\Scripts\activate```

## Skonfiguruj bazę danych

W pliku mga_zadanie/settings.py znajdź sekcję DATABASES i dostosuj ją do swoich ustawień PostgreSQL:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Stworzyć bazę danych o podanej wcześniej nazwię w pliku setting.py

Przez pg4Admin wystarczy kliknąć prawym przyciskiem myszy w Databases i utworzyć nową bazę danych
Lub używając psql i po zalogowaniu wpisać komendę CREATE DATABASE 'your_db_name'

## Instalacja zależności

```pip install -r requirements.txt```

## Zrób migracje danych

```python manage.py makemigrations```
```python manage.py migrate```


## Dodaj superużytkownika

```python manage.py createsuperuser```

## Uruchom serwer

```python manage.py runserver```


# API

- `POST /api/tasks/` - dodawanie zadania
- `PUT /api/tasks/{id}/` - edytowanie zadania
- `GET /api/tasks/` - lista zadań
- `GET /api/tasks/{id}/` - szczegóły zadania
- `DELETE /api/tasks/{id}/` - usuwanie zadania
- `GET /api/tasks/{id}/history/` - historia zmian zadania
- `POST /api/register/`- rejestracja użytkownika
- `POST /api/token/` - logowanie użytkownika(token)


### Przykłady użycia API przy pomocy curl

- Rejestracja użytkownika:

```bash
curl -X POST http://localhost:8000/api/register/ -d "{\"username\":\"your_username\",\"password\":\"your_password\",\"email\":\"your_email\"}" -H "Content-Type: application/json"
```

- Logowanie użytkownika:
Żeby zadania były widoczne dla danego użytkownika trzeba się zalogować

```bash
curl -X POST http://localhost:8000/api/token/ -d "{\"username\":\"your_username\",\"password\":\"your_password\"}" -H "Content-Type: application/json"
```
Po wpisaniu komendy wyswietli się token 'access', który bedzie trzeba wpisywać jako autentykacja

- Dodanie zadania:
```bash
curl -X POST http://localhost:8000/api/tasks/ -d "{\"name\":\"task_name\",\"description\":\"task_description\", \"status\": \"{Nowy,W toku lub Rozwiązany}\", \"assigned_user\": <number user> }" -H "Content-Type: application/json" -H "Authorization: Bearer your_access_token"
```

- Edycja zadania:
```bash
curl -X PUT http://localhost:8000/api/tasks/{id}/ -d "{\"name\":\"task_name\",\"description\":\"task_description\", \"status\": \"{Nowy,W toku lub Rozwiązany}\", \"assigned_user\": <number user> }" -H "Content-Type: application/json" -H "Authorization: Bearer your_access_token"
```
- Lista zadań:
```bash
curl -X GET http://localhost:8000/api/tasks/ -H "Content-Type: application/json" -H "Authorization: Bearer your_access_token"
```
- Szczegóły zadania:
```bash
curl -X GET http://localhost:8000/api/tasks/{id}/ -H "Content-Type: application/json" -H "Authorization: Bearer your_access_token"
```
- Usuwanie zadania:
```bash
curl -X DELETE http://localhost:8000/api/tasks/{id}/ -H "Content-Type: application/json" -H "Authorization: Bearer your_access_token"
```
- Historia zmian:
```bash
curl -X GET http://localhost:8000/api/history/ -H "Content-Type: application/json" -H "Authorization: Bearer your_access_token"
```
- Historia zmian zadania:
```bash
curl -X GET http://localhost:8000/api/history/{id}/ -H "Content-Type: application/json" -H "Authorization: Bearer your_access_token"
```
- Filtrowanie zadań:

Przykład - komenda zwróci zadania przypisane do zalogowanego użytkownika których status to "Nowy" oraz przypisany użytkownik jest równy null
```bash
curl -X GET "http://localhost:8000/api/tasks/?status=Nowy&assigned_user__isnull=true" -H "Content-Type: application/json" -H "Authorization: Bearer your_access_token"
```
Przyklad - komenda zwróci historię zmian zadań, które mają status "Nowy" oraz w nazwie zawiera się słowo "test"
```bash
curl -X GET "http://localhost:8000/api/history/?status=Nowy&name_icontains=test" -H "Content-Type: application/json" -H "Authorization: Bearer your_access_token"
```

# Pytest

## Uruchamianie Testów

```pytest```