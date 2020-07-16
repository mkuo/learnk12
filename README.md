
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
    postgres=# ALTER USER admin CREATEDB;
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
Django, Gunicorn and Nginx were initially set up according to [this guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04).  
Let's Encrypt SSL was initially set up according to [this guide](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04).  
DDOS mitigatios was initially set up according to [this guide](https://www.nginx.com/blog/mitigating-ddos-attacks-with-nginx-and-nginx-plus/)

1. Set up ssh access to the remote server on DigitalOcean.
2. Generate ssh keys for your Github account and [use ssh agent forwarding](https://developer.github.com/v3/guides/using-ssh-agent-forwarding/).
3. Pull code from this repo.

To run custom Django commands, see command files in `learnk12/home/management/commands`.
```
(venv) [mike@learnk12 learnk12 (master)]$ ./manage.py update_courses_agg_fields
```

# Production Debugging and Logging
```
$ ssh mike@learnk12.org

# Check service statuses
[mike@learnk12 ~ ]$ sudo systemctl status postgresql
[mike@learnk12 ~ ]$ sudo systemctl status gunicorn
[mike@learnk12 ~ ]$ sudo systemctl status nginx
[mike@learnk12 ~ ]$ sudo ufw status

# Check nginx connections
[mike@learnk12 ~ ]$ curl https://www.learnk12.org/nginx_status

# Check logs
[mike@learnk12 ~ ]$ tail ~/projects/learnk12/log
[mike@learnk12 ~ ]$ sudo journalctl -u nginx
[mike@learnk12 ~ ]$ sudo tail /var/log/nginx/access.log
[mike@learnk12 ~ ]$ sudo tail /var/log/nginx/error.log
[mike@learnk12 ~ ]$ sudo journalctl -u gunicorn
[mike@learnk12 ~ ]$ sudo journalctl -u gunicorn.socket

# Check production settings
[mike@learnk12 ~ ]$ nano ~/projects/learnk12/learnk12/settings/local.py
[mike@learnk12 ~ ]$ nano /etc/systemd/system/gunicorn.socket
[mike@learnk12 ~ ]$ nano /etc/systemd/system/gunicorn.service
[mike@learnk12 ~ ]$ nano /etc/nginx/sites-available/learnk12
```

# Production Deploy
To deploy new code, use the zshell script `deploy.sh`.
```
# authenticate with GitHub
$ ssh -T git@github.com
$ ssh mike@learnk12.org

# manually run first time only to pull the deploy.sh script 
[mike@learnk12 ~ ]$ cd ~/projects/learnk12
[mike@learnk12 learnk12 (master)]$ git pull

[mike@learnk12 ~ ]$ echo -n 'alias deploy="zsh ~/projects/learnk12/deploy.sh"' >> ~/.zshrc
[mike@learnk12 ~ ]$ source ~/.zshrc
```
