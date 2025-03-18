# video-platform-k8s

1. Installing k3s on Windows if you don't have it already
Since k3s runs on Linux, you need WSL2 (Windows Subsystem for Linux) with Ubuntu.

Step 1: Install WSL2 (If Not Installed)
Open PowerShell as Administrator and run:

command: wsl --install -d Ubuntu

/ubuntu is the standard so specifying this isn't needed but other options do exist, keep the -d and behind it pick another if you so wish/

Restart your computer if needed.
Open Ubuntu (WSL2 terminal) and set up a username/password.

Step 2: Install k3s
In the WSL2 Ubuntu terminal, install k3s:

command: curl -sfL https://get.k3s.io | sh -

Verify the installation:

command: kubectl get nodes

You should see one node (Ready status), meaning k3s is running. If all is well k3s is now succesfully installed on your device.

2. Installing react 

route in the terminal to the front-end map 

command: npm install

3. Pyhton flask API