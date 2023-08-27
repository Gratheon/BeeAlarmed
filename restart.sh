cd /www/models-gate-tracker/
COMPOSE_PROJECT_NAME=gratheon docker-compose down

chown www:www-data -R /www/models-gate-tracker
sudo -H -u www bash -c 'cd /www/models-gate-tracker/' 
COMPOSE_PROJECT_NAME=gratheon docker-compose up -d --build