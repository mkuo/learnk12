
# Development Environment Setup
1. Create your local Postgres database with `psql`
	```
	$ psql postgres
	postgres=# CREATE DATABASE learnk12;
	postgres=# CREATE USER admin;
	postgres=# ALTER ROLE admin SET client_encoding TO 'utf8';
	postgres=# ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
	postgres=# ALTER ROLE admin SET timezone TO 'UTC';
	postgres=# GRANT ALL PRIVILEGES ON DATABASE learnk12 TO admin;
	postgres=# \q
	```
2. Clone this repo.
3. Make sure you are running Python3. If you are on a Mac, use [pyenv](https://github.com/pyenv/pyenv).
4. Install requirements within a virtual environment in the project directory
	```
	learnk12 $ virtualenv venv
	learnk12 $ source venv/bin/activate
	(venv) learnk12 $ pip install -r requirements.txt
	```
5. Run database migrations
	```
	(venv) learnk12 $ ./manage.py migrate
	```
6. Run the application server locally
	```
	(venv) learnk12 $ ./manage.py runserver
	```
7. Access the application at [http://localhost:8000/](http://localhost:8000/)

# Production Environment Setup
Gunicorn, nginx, and SSL settings were initially set up according to [this guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04).

1. Set up ssh access to the remote server on DigitalOcean.
2. Generate ssh keys for your Github account and [use ssh agent forwarding](https://developer.github.com/v3/guides/using-ssh-agent-forwarding/).
3. Pull code from this repo.

To deploy new code
```
$ ssh mike@learnk12.org
[mike@learnk12 ~ ]$ cd projects/learnk12
[mike@learnk12 learnk12 (master)]$ git pull

[mike@learnk12 learnk12 (master)]$ source venv/bin/activate

# if there are new python packages in the deploy 
(venv) [mike@learnk12 learnk12 (master)]$ pip install -r requirements.txt

# if there are new or updated static files in the deploy 
(venv) [mike@learnk12 learnk12 (master)]$ ./manage.py collectstatic

# if there are database migrations in the deploy
(venv) [mike@learnk12 learnk12 (master)]$ ./manage.py migrate

# gracefully restart gunicorn app serving
[mike@learnk12 learnk12 (master)]$ sudo systemctl reload gunicorn
```

To run custom Django commands, see command files in `learnk12/home/management/commands`.
```
(venv) [mike@learnk12 learnk12 (master)]$ ./manage.py update_courses_agg_fields
```
