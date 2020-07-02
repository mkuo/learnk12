#!/bin/zsh
cd ~/projects/learnk12
git pull
source venv/bin/activate
export DJANGO_SETTINGS_MODULE="learnk12.settings.production"
./manage.py check --deploy
zsh deploy_commands.sh
