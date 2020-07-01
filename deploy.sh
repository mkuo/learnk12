#!/bin/zsh
confirm () {
    read "reply?$1 (y/n)? "
    if [[ $reply =~ ^[Yy]$ ]]; then $2; fi
}

install_requirements () { pip install -r requirements.txt }
collect_static_files () { ./manage.py collectstatic }
migrate_database () { ./manage.py migrate }
reload_nginx () { sudo systemctl reload nginx }
reload_gunicorn () { sudo systemctl reload gunicorn }
clear_sessions () { ./manage.py clearsessions }
update_courses_agg_fields () { ./manage.py update_courses_agg_fields }
check_unused_images () { ./manage.py check_unused_images }

cd ~/projects/learnk12
git pull
source venv/bin/activate
export DJANGO_SETTINGS_MODULE="learnk12.settings.production"
./manage.py check --deploy

confirm "Update dependencies" install_requirements;
confirm "Collect static files" collect_static_files;
confirm "Run migrations" migrate_database;
confirm "Reload nginx" reload_nginx;
confirm "Reload gunicorn" reload_gunicorn;

echo "Now suggesting optional manual cleanup commands..."
confirm "Clear expired sessions" clear_sessions;
confirm "Update courses aggregate fields" update_courses_agg_fields
confirm "Check unused images" check_unused_images