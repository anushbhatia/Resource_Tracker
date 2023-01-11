# Resource_Tracker
## Prerequisites
```
Python
mysql
```
## Installation Instruction
1. ```pip install -r requirements.txt```
2. Check the settings.py present in resource tracker for the credentials for mysql and change them if required.
```python manage.py migrate```
3. Run the below commands: 
```python manage.py makemigrations employee_register```
```python manage.py sqlmigrate employee_register 0001```
```python manage.py migrate```
4. Load initial data (create groups and assign permission)
```./manage.py shell```
```exec(open('employee_register\initial_script.py').read())```
5. To run server
 ```python manage.py runserver```

