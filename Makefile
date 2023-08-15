start:
	COMPOSE_PROJECT_NAME=gratheon docker compose -f docker-compose.dev.yml up --build
stop:
	COMPOSE_PROJECT_NAME=gratheon docker compose -f docker-compose.dev.yml down

# deploy-copy:
# 	rsync -av -e ssh * root@gratheon.com:/www/models-frame-resources/

# deploy-run:
# 	ssh root@gratheon.com 'chmod +x /www/models-frame-resources/restart.sh'
# 	ssh root@gratheon.com 'bash /www/models-frame-resources/restart.sh'

# deploy:
# 	make deploy-copy
# 	make deploy-run