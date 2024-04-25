#!/bin/bash

# Pull the latest images
echo "Pulling Docker images..."
docker pull <YOUR_DOCKERHUB_USERNAME>/<FRONTEND_PROJECT>:<TAG>
docker pull <YOUR_DOCKERHUB_USERNAME>/<BACKEND_PROJECT>:<TAG>
docker pull <YOUR_DOCKERHUB_USERNAME>/<NGNINX_PROJECT>:<TAG>

# Stopping and removing all containers
docker stop $(docker ps -q)
docker rm -f $(docker ps -aq)


# Check if the network exists
if [ ! "$(docker network ls | grep my-app-network)" ]; then
  echo "Creating new Docker network: my-app-network"
  docker network create my-app-network
else
  echo "Docker network 'my-app-network' already exists."
fi

# Run the containers
echo "Running Docker containers..."
docker run -d --network my-app-network --name backend \
-e GPT_APIKEY=<YOUR_API_KEY> \
-e GPT_MODEL_NAME=gpt-4-turbo \
<YOUR_DOCKERHUB_USERNAME>/<BACKEND_PROJECT>:<TAG>

docker run -d --network my-app-network --name frontend <YOUR_DOCKERHUB_USERNAME>/<FRONTEND_PROJECT>:<TAG>
docker run -d --network my-app-network --name nginx -p 80:80 <YOUR_DOCKERHUB_USERNAME>/<NGNINX_PROJECT>:<TAG>

echo "Setup completed successfully."
