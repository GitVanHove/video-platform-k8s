# **Video Platform (Kubernetes & Docker)**

## **Project overview**

This is a web-based video platform that allows users to upload, manage, and analyze videos using an AI model.
The frontend runs in the browser at http://localhost:3000, while the backend runs at http://127.0.0.1:5000.

## **Installation Instructions**  

To install and run this project, follow these steps:

### **1. Clone the Repository**  
```sh
git clone https://github.com/yourusername/video-platform-k8s.git
cd video-platform-k8s
```

### **2. Run the Project with Docker**  
Ensure you have **Docker Desktop** (Windows/macOS) or **Docker Engine** (Linux) installed.  
Then, run the following command in the root directory (where `docker-compose.yml` is located):  

```sh
docker-compose up --build
```

⚠ **Note:** The AI model required for this project is over **6GB** in size.  
The initial setup may take a while as it downloads and sets up dependencies.

---

### **3. Close the project**  
You can use ctrl+c stop the project and then use this command to close all running containers 

```sh
docker-compose down
```

---

## **Predefined Users**  
The project includes a few hardcoded users for testing:

| Username | Password  |
|----------|----------|
| admin    | admin123 |
| user1    | password1 |
| user2    | password2 |

You can log in using one of these credentials.

---

## **Prerequisites**  
Before running this project, ensure you have:  

✅ **Docker Desktop / Docker Engine** installed.  
✅ A stable internet connection for the first-time setup.  

---

## **Video project**  
 youtube: https://youtu.be/oFRQjO3ob0w
 drive: https://drive.google.com/file/d/15nhtGChcGOYo-ISTj5IrluK3UlDi3xz7/view?usp=drive_link
---