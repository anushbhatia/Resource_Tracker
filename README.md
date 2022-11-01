# Resource_Tracker
## Prerequisites
```
Python
Postgres
pgadmin 4
```
## Installation Instruction
1. ```pip install -r requirements.txt```
2. Check the settings.py present in resource tracker for the credentials for postgres and change them if required.
3. ```python manage.py migrate```
4. Run the below commands: 
```` 
python manage.py makemigrations employee_register
python manage.py sqlmigrate employee_register 0001
python manage.py migrate 
````
5. ```python manage.py runserver```

