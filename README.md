# CIS465_Project

This is the repository for our Multimedia Project and will contain an application that:

* Calculates Entropy and redundancy from user given image
* Performs a transformation or two
* Provides a simple front end interface


## Use instructions 

* To start the application ensure you have django installed using `python -m pip install Django`
* Once installed, simply run `python manage.py runserver` to start up the built in local server used by django 
* This should by default start running on port 8000 so navigate to 'http://127.0.0.1:8000/' or just 'http://localhost:8000/'

## Notes

* Sometimes the local db django has doesnt sync properly, if the error is about a table not existing or a DB issue try running `python manage.py makemigrations` and `python manage.py migrate --run-syncdb` this should sync it up and create the tables if needed. If that doesn't work it could be some other issue but I dont anticipate that