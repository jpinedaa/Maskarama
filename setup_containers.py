import os
import time
from utils import base_dir
import docker

def export_container(client, container_name, export_path, image_name=None):
    try:
        container = client.containers.get(container_name)
        print(f"Committing container {container_name} to a new image...")

        # Commit the container to a new image
        if image_name is None:
            image_name = container_name
        image = container.commit(repository=image_name)
        print(f"Committed to image {image.id}")

        print(f"Saving image {image.id} to {export_path}...")
        # Save the committed image to a tar file
        with open(export_path, 'wb') as export_file:
            for chunk in image.save():
                export_file.write(chunk)

        print(f"Image saved to {export_path}")
    except docker.errors.NotFound:
        print(f"Container {container_name} not found. Cannot export.")
    except docker.errors.APIError as e:
        print(f"An error occurred: {e}")


def import_container(client, import_path, image_name):
    print(f"Loading image from {import_path}...")
    with open(import_path, 'rb') as import_file:
        image = client.images.load(import_file.read())
    image[0].tag(image_name)
    print(f"Image loaded: {image[0].id}, name: {image_name}")
    return image[0]


def start_or_create_container(client, container_name, image_name, port1, port2):
    try:
        container = client.containers.get(container_name)
        if container.status != 'running':
            print(f"Starting existing container {container_name}...")
            container.start()
        else:
            print(f"Container {container_name} is already running.")
    except docker.errors.NotFound:
        print(f"Container {container_name} not found. Creating new container...")
        container = client.containers.run(
            image_name,
            name=container_name,
            detach=True,
            ports={'7474/tcp': port1 , '7687/tcp': port2},
            environment={
                'NEO4J_apoc_export_file_enabled': 'true',
                'NEO4J_apoc_import_file_enabled': 'true',
                'NEO4J_apoc_import_file_useneo4jconfig': 'true',
                'NEO4J_AUTH': 'neo4j/password',
                'NEO4J_PLUGINS': '["apoc"]'
            }
        )
        print(f"New container {container_name} created and started.")
    return container


def setup_memory_containers():
    client = docker.from_env(timeout=600)
    containers_dir = os.path.join(base_dir, "memory_containers")

    memory_map = {}
    port1 = 7474
    port2 = 7687
    for container in os.listdir(containers_dir):
        if container.endswith(".tar"):
            import_path = os.path.join(containers_dir, container)
            image_name = container.replace(".tar", "")
            try:
                client.images.get(image_name)
                print(f"Image {image_name} already exists.")
            except docker.errors.ImageNotFound:
                print(f"importing image {image_name}...")
                import_container(client, import_path, image_name)
            start_or_create_container(client, image_name, image_name, port1, port2)
            port1 += 1
            port2 += 1

    return memory_map


if __name__ == '__main__':
    setup_memory_containers()