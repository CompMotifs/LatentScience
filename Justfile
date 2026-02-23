default:
    @just --list

fix dir="latentscience":
    uv run ruff format {{dir}}
    uv run ruff check --fix {{dir}}

lint dir="latentscience":
    uv run ruff check {{dir}}
    uv run pyright {{dir}}

lint-file file:
    - uv run ruff check {{file}}
    - uv run pyright {{file}}


#####################################
### DOCKER COMMANDS ###
#####################################

# Environment configuration
LOCAL_ENV := "--env-file ../.env.local"

docker-build tag="latentscience:latest":
    docker build -t {{tag}} .

docker-run tag="latentscience:latest" port="8000":
    docker run -d --name latentscience -p {{port}}:8000 {{tag}}

docker-shell tag="latentscience:latest":
    docker run -it --rm {{tag}} bash

docker-stop:
    docker stop latentscience || true
    docker rm latentscience || true

docker-logs:
    docker logs -f latentscience

docker-restart: docker-stop docker-run

docker-clean:
    docker stop latentscience || true
    docker rm latentscience || true
    docker rmi latentscience:latest || true


#####################################
### LOCAL DEVELOPMENT ENVIRONMENT ###
#####################################

[working-directory: 'infra']
local-setup:
    mkdir -p postgres/init logs
    @echo "Setup directories created."

[working-directory: 'infra']
local-build:
    docker compose {{LOCAL_ENV}}  build

[working-directory: 'infra']
local-up:
    # Start all services - docker compose will handle dependencies via health checks
    docker compose {{LOCAL_ENV}}  up -d --build

[working-directory: 'infra']
local-shell:
    # Start services if not running
    docker compose {{LOCAL_ENV}}  exec api bash

[working-directory: 'infra']
local-down:
    docker compose {{LOCAL_ENV}}  down -v

[working-directory: 'infra']
local-logs service="":
    @echo "Fetching logs from all services..."
    docker compose {{LOCAL_ENV}}  logs -f {{service}}

[working-directory: 'infra']
local-ps:
    docker compose {{LOCAL_ENV}}  ps

[working-directory: 'infra']
local-restart-api:
    @echo "Restarting API service (keeps ngrok URL)..."
    docker compose {{LOCAL_ENV}}  restart api

[working-directory: 'infra']
local-rebuild-api:
    @echo "Rebuilding and restarting API service (keeps ngrok URL)..."
    docker compose {{LOCAL_ENV}}  up -d --build api

[working-directory: 'infra']
local-wipe:
    @echo "Wiping PostgreSQL database data..."
    rm -rf db/data || true
    @echo "Database data has been wiped."

[working-directory: 'infra']
local-stop SVC:
    @echo "Stopping service {{SVC}}..."
    docker compose {{LOCAL_ENV}}  stop {{SVC}}
    @echo "Service {{SVC}} stopped."

local-refresh: local-down local-wipe local-up

[working-directory: 'infra']
local-refresh-app:
    @echo "Taking down all services except ngrok..."
    docker compose {{LOCAL_ENV}}  rm -sf db auth rest storage imgproxy api kong
    @echo "Wiping database data..."
    rm -rf db/data || true
    @echo "Starting services back up..."
    docker compose {{LOCAL_ENV}}  up -d --build

[working-directory: 'infra']
local-psql:
    docker compose {{LOCAL_ENV}}  exec db psql -U postgres -d postgres

[working-directory: 'infra']
local-populate:
    docker compose {{LOCAL_ENV}}  exec api python -m latentscience --populate
