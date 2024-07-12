import docker
import os

SYS_PROJECT_DIR  = "/home/matatov.n/mlops_projects/mllmcd"

client = docker.from_env()
client.containers.list()

image_name = "mllmcd:latest"

container = client.containers.run(
    image=image_name,
    device_requests=[docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])],  # Specify GPU access
    volumes=volumes,
    stdin_open=True,  # -it
    tty=True,  # -it
    remove=True,  # --rm
    detach=True  # Run in detached mode to capture the container object
)

# Print the container ID
print(f"Running container ID: {container.id}")

# docker exec -it 8983bd7f7175fdc30d1fc67ac08d21e0e2ab586d52753d2a87cc2f6ae0e71249 /bin/bash

# Execute the script inside the container
_, stream = container.exec_run(script_command, stream=True)

# Print the execution log
for data in stream:
    print(data.decode())

container.stop()

print(f'Container run finished')
