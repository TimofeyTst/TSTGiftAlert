#!/usr/bin/env bash

# Load variables from .env file located in project root (if exists)
ENV_FILE="$(dirname "$0")/../.env"
if [[ -f "$ENV_FILE" ]]; then
  export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# Verify required variables
: "${RESOURCES__POSTGRES__USER:?Need RESOURCES__POSTGRES__USER in .env}" 
: "${RESOURCES__POSTGRES__PASSWORD:?Need RESOURCES__POSTGRES__PASSWORD in .env}" 
: "${RESOURCES__POSTGRES__HOST:?Need RESOURCES__POSTGRES__HOST in .env}" 
: "${RESOURCES__POSTGRES__PORT:?Need RESOURCES__POSTGRES__PORT in .env}" 
: "${RESOURCES__POSTGRES__DATABASE_NAME:?Need RESOURCES__POSTGRES__DATABASE_NAME in .env}" 

DSN="postgresql://${RESOURCES__POSTGRES__USER}:${RESOURCES__POSTGRES__PASSWORD}@${RESOURCES__POSTGRES__HOST}:${RESOURCES__POSTGRES__PORT}/${RESOURCES__POSTGRES__DATABASE_NAME}"

echo "Applying migrations"
poetry run yoyo-migrate apply -d "$DSN" migrations
