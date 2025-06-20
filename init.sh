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

