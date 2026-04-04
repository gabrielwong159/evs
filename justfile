set dotenv-load

[private]
default:
  @just --list

# Run the main API server for the web app
[group('run')]
main-dev:
  uv run flask --app app.main run

# Run the main API server for the web app with gunicorn
[group('run')]
main-prod:
  uv run gunicorn -b 127.0.0.1:8080 app.main:app

# Run the scheduled task to scrape balances from the web
[group('run')]
scraper:
  uv run python -m app.scripts.scraper

# Run the scheduled task to create balance notifications
[group('run')]
notify:
  uv run python -m app.scripts.notify

# Run the Telegram bot in polling mode
[group('run')]
telebot:
  uv run python -m app.scripts.telebot

[group('dev')]
test:
  uv run pytest tests/

[group('dev')]
db-shell:
  docker compose exec db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
