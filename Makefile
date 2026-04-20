include .env

.PHONY: up db-shell certbot-init certbot-renew

up:
	docker compose up -d nginx telebot grafana

db-shell:
	docker compose exec db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

certbot-init:
	docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d api.evs.gabrielwong.dev -v

certbot-renew:
	docker compose run --rm certbot renew
