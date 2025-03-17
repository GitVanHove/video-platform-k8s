#!/bin/bash

echo "🛑 Stopping Kubernetes Pods..."
sudo kubectl delete -f k3s/backend-deployment.yaml

echo "🐳 Stopping & Removing Docker Containers..."
docker-compose down

echo "🗑️ Removing unused Docker images & containers..."
docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -aq)

echo "✅ Cleanup complete!"