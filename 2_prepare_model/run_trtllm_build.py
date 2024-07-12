import docker
import os

SYS_PROJECT_DIR  = "/home/matatov.n/mlops_projects/mllmcd"

client = docker.from_env()
client.containers.list()

image_name = "mllmcd:latest"
conversion_path = os.path.join(SYS_PROJECT_DIR, "2_prepare_model/conversion")
compilation_path = os.path.join(SYS_PROJECT_DIR, "2_prepare_model/compilation")

# Define mount paths
volumes = {
    # Output path
    conversion_path : {
        'bind' : os.path.join("/mnt", "data",  "conversion"),
        'mode' : 'ro'
    },
    # Compiled model path
    compilation_path : {
        'bind' : os.path.join("/mnt", "data",  "compilation"),
        'mode' : 'rw'
    }
}

script_command = f"""trtllm-build \
--checkpoint_dir {volumes[conversion_path]['bind']} \
--output_dir {volumes[compilation_path]['bind']} \
--gpt_attention_plugin bfloat16 \
--gemm_plugin bfloat16
"""

# # Define the base command to run the Docker container
# docker_command = 'docker run --rm --runtime=nvidia --gpus all --entrypoint /bin/bash -it nvidia/cuda:12.1.0-devel-ubuntu22.04'

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

# docker exec -it 96c043a5cd50 /bin/bash

# Execute the script inside the container
_, stream = container.exec_run(script_command, stream=True)

# Print the execution log
for data in stream:
    print(data.decode())

container.stop()

print(f'Container run finished')
