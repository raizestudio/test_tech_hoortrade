#!/bin/env bash
set -e  # :(

USE_DOCKER=false
RESET_DOCKER=false

for arg in "$@"; do
  case $arg in
    --docker)
      USE_DOCKER=true
      ;;
    --reset-docker)
      RESET_DOCKER=true
      ;;
  esac
done

# Check if .env file exists; if not, copy from .env.example
if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
  else
    echo "ERROR: .env.example not found. Cannot initialize .env."
    exit 1
  fi
fi

# Load .env variables into the environment
set -a
source .env
set +a

# Check if TMDB_API_KEY is set
if [ -z "$TMDB_API_KEY" ]; then
  echo "TMDB_API_KEY is not set in the .env file."

  if [ -t 0 ]; then  # Check for interactive shell
    read -p "Do you want to enter it now? [Y/n]: " answer
    answer=${answer:-Y}

    if [[ "$answer" =~ ^[Yy]$ ]]; then
      read -p "Enter TMDB_API_KEY: " tmdb_key

      tmdb_key_escaped=$(printf '%q' "$tmdb_key")
      sed -i.bak '/^TMDB_API_KEY=/d' .env
      echo "TMDB_API_KEY=\"$tmdb_key_escaped\"" >> .env

      # Reload env vars
      set -a
      source .env
      set +a
    else
      echo "Continuing without TMDB_API_KEY (third-party API may not work properly)."
    fi
  else
    echo "Non-interactive shell detected; skipping prompt for TMDB_API_KEY."
    echo "You can manually set it in the .env file if needed."
  fi
fi

if [ "$USE_DOCKER" = true ] || [ "$RESET_DOCKER" = true ]; then
  echo "Setting DATABASE_URL for Docker..."
  sed -i.bak '/^DATABASE_URL=/d' .env
  echo 'DATABASE_URL="psql://hoortrade:hoortrade@db:5432/hoortrade"' >> .env

  # Reload .env with updated value
  set -a
  source .env
  set +a
fi

if [ "$RESET_DOCKER" = true ]; then
  echo "Resetting Docker containers and volumes..."
  cd docker/
  docker compose down -v --remove-orphans
  docker compose build --no-cache
  docker compose up -d
  cd -
elif [ "$USE_DOCKER" = true ]; then
  echo "Starting Docker containers..."
  cd docker/
  docker compose up -d
  cd -
exit 0
fi

# Create necessary directories
mkdir -p logs
mkdir -p media

chmod -R 755 logs media

echo "Initialized logs/ and media/ directories."

