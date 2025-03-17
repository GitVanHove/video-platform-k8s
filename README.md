# video-platform-k8s

🚀 Start Docker & Kubernetes (K3s)
1️⃣ Start Docker
Run this in Ubuntu:
go to  -> /mnt/c/Users/(user)/Documents/GitHub/video-platform-k8s

chmod +x k3s/start.sh k3s/stop.sh

# Manual start up

sudo systemctl start docker
Check if Docker is running:

sudo systemctl status docker
If you see "active (running)", you're good to go.

2️⃣ Build & Load the Image

(In back-end)
docker build -t video-platform-backend .

3️⃣ Apply the Deployment in K3s

sudo kubectl apply -f backend-deployment.yaml

sudo kubectl get pods

🛑 Stop Everything & Free RAM
1️⃣ Stop Kubernetes Pods

sudo kubectl delete -f backend-deployment.yaml
2️⃣ Remove Docker Containers & Images
List all running containers:

docker ps -a

Remove all containers:

docker rm -f $(docker ps -aq)

Remove all images:

docker rmi -f $(docker images -aq)

3️⃣ Stop Docker

sudo systemctl stop docker