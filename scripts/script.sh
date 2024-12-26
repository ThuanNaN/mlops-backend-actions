#/bin/bash

set -e  # Exit on any command failure
set -o pipefail  # Ensure pipelines return an error if any command fails

echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

docker pull thuannan/fastapi-backend:latest

docker stop fastapi-backend || echo "Container not running, proceeding..."

docker rm fastapi-backend || echo "Container not found, proceeding..."

docker run -d -p 80:8000 --name fastapi-backend thuannan/fastapi-backend:latest
