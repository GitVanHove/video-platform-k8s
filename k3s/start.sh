#!/bin/bash

echo "🚀 Is Docker desktop on?..."

echo "🐳 Building & Running Docker Containers..."
docker-compose --profile ignore up --build -d

echo "☸️  Deploying to Kubernetes..."
sudo kubectl apply -f k3s/backend-deployment.yaml --validate=false

echo "✅ All services are up and running!"