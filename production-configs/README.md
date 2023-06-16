# Enable rh-node to run on a new system with knowledge of each other

## Prepare yaml config
- `sudo mkdir -p /etc/docker/compose/rh-node`
- Copy `docker-compose.TEMPLATE.yaml` to that folder and rename it to `/etc/docker/compose/rh-node/docker-compose.yaml`
- Edit the yaml file so only the services that should be available on the system remains
- If the node is part of a cluster of nodes, add the other nodes in the field `RH_OTHER_ADDRESSES`
- Edit the fields `RH_NAME` `RH_MEMORY` `RH_GPU_MEM` and `RH_NUM_THREADS` under `manager` service so it fits your system.
  
  Hints:
    - `RH_NAME` can be found with `hostname`
    - `RH_MEMORY` can be found with `free -g`
    - `RH_GPU_MEM` can be found with `nvidia-smi`
    - `RH_NUM_THREADS` can be found with `nproc`
## Install with systemd
- Copy the systemd file to the systemd folder: `sudo cp docker-compose@.service /etc/systemd/system/`
- Start your systemd `systemctl start docker-compose@rh-node`



