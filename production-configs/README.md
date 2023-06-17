# Enable rh-node to run on a new system

## Install Docker
### Set up the repository
1. Update the apt package index and install packages to allow apt to use a repository over HTTPS:
   ```
   sudo apt-get update
   sudo apt-get install -y ca-certificates curl gnupg
   ```
2. Add Docker’s official GPG key:
   ```
   sudo install -m 0755 -d /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   sudo chmod a+r /etc/apt/keyrings/docker.gpg
   ```
3. Use the following command to set up the repository:
   ```
   echo \
   "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
   "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```
### Install Docker Engine
1. Update the apt package index:
   
   ```sudo apt-get update```
2. Install Docker Engine, containerd, and Docker Compose.
  
   ```sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin```
3. Verify that the Docker Engine installation is successful by running the hello-world image.
   
   ```sudo docker run hello-world```

### Install CUDA with Docker
1. Add the toolkit’s package repository to your system using the example command:

   ```
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID) 
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - 
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   ```
2. Next install the nvidia-docker2 package on your host:

   ```
   sudo apt-get update
   sudo apt-get install -y nvidia-docker2
   ```
3. Restart the Docker daemon to complete the installation:

   ```
   sudo systemctl restart docker
   ```
4. You might need to add your user to the docker group to gain correct permissions. To do so, run:
   
   ```
   sudo groupadd docker
   sudo usermod -aG docker ${USER}
   ```
   
   Login and log-out, e.g. using `su -s ${USER}`
5. Test install
   
   ```
   docker run -it --gpus all nvidia/cuda:11.4.0-base-ubuntu20.04 nvidia-smi
   ```
   


## Prepare yaml config
- `sudo mkdir -p /etc/docker/compose/rh-node`
- Copy `docker-compose.TEMPLATE.yaml` to that folder and rename it to `/etc/docker/compose/rh-node/docker-compose.yaml`
- Edit the yaml file so only the services that should be available on the system remains
- If the node is part of a cluster of nodes, add the other nodes in the field `RH_OTHER_ADDRESSES` under `manager` service
- Edit the fields `RH_NAME` `RH_MEMORY` `RH_GPU_MEM` and `RH_NUM_THREADS` under `manager` service so it fits your system.
  
  Hints:
    - `RH_NAME` can be found with `hostname`
    - `RH_MEMORY` can be found with `free -g`
    - `RH_GPU_MEM` can be found with `nvidia-smi`
    - `RH_NUM_THREADS` can be found with `nproc`
- <b>IMPORTANT:</b> The ports under the `reverse-proxy` defines if the node is a production node or research:
  - 9030 & 9031: Research node
  - 9040 & 9041: Production node
  - 9050 & 9051: Used to develop nodes that are not expected to be live at all times (and therefore should not have a systemd file!)
   
## Install with systemd
- Copy the systemd file to the systemd folder: `sudo cp docker-compose@.service /etc/systemd/system/`
- Start your systemd `systemctl start docker-compose@rh-node`




