include .env

.DEFAULT_GOAL:=help

.PHONY: up db-shell help

up:  ## Start necessary services for app
	docker compose up -d caddy telebot grafana

db-shell:  ## Create Postgres shell
	docker compose exec db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
