#!/bin/zsh
confirm () {
    read "reply?$1 (y/n)? "
    if [[ $reply =~ ^[Yy]$ ]]; then eval $2; fi
}

echo "Running production deploy commands..."
confirm "Update dependencies" 'pip install -r requirements.txt';
confirm "Collect static files" './manage.py collectstatic';
confirm "Run migrations" './manage.py migrate';
confirm "Reload nginx" 'sudo systemctl reload nginx';
confirm "Reload gunicorn" 'sudo systemctl reload gunicorn';

echo "Now suggesting optional manual cleanup commands..."
confirm "Clear expired sessions" './manage.py clearsessions';
confirm "Update courses aggregate fields" './manage.py update_courses_agg_fields';
confirm "Check unused images" './manage.py check_unused_images';
confirm "Check oversized course images" './manage.py check_oversized_course_images';
