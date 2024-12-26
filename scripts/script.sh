#/bin/bash

# echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

docker pull thuannan/fastapi-backend:latest
docker stop fastapi-backend || true
docker rm fastapi-backend || true
docker run -d -p 80:8000 --name fastapi-backend thuannan/fastapi-backend:latest
