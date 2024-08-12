import os
import time
from utils import base_dir
import docker
from memory import MEMORY_MAP


def wait_for_container(container, timeout=30):
    """Wait for a container to be ready."""
    for _ in range(timeout):
        container.reload()
        if container.status == 'running':
            return True
        time.sleep(1)
    return False


def export_database(container_name, export_path):
    try:
        client = docker.from_env(timeout=600)
        container = client.containers.get(container_name)
        print(f"Stopping the container {container_name} to export the database...")

        # Stop the entire container
        container.stop()

        # Export the database using docker cp to avoid issues with container stopping
        print(f"Exporting database from container {container_name} to {export_path}...")

        # Ensure the directory for the dump exists in the container
        dump_dir = '/data/backup_dir'
        container.start()
        container.exec_run(f'mkdir -p {dump_dir}')
        container.stop()

        # Run the export command inside the container using `docker exec` after container restart
        export_command = f"bin/neo4j-admin database dump neo4j --to-path={dump_dir}"
        container.start()
        exit_code, output = container.exec_run(export_command)
        container.stop()

        if exit_code != 0:
            print(f"Failed to export database: {output.decode('utf-8')}")
            return

        # Archive the directory into a single file to copy it out (using tar only, not gzip)
        archive_command = f'tar -cvf /data/backup.dump.tar -C {dump_dir} .'
        container.start()
        container.exec_run(archive_command)
        container.stop()

        # Copy the dump file from the container to the host
        with open(export_path, 'wb') as export_file:
            bits, _ = container.get_archive('/data/backup.dump.tar')
            for chunk in bits:
                export_file.write(chunk)

        print(f"Database exported to {export_path}")

        # Restart the container after exporting
        container.start()
        print(f"Container {container_name} restarted successfully.")

    except docker.errors.NotFound:
        print(f"Container {container_name} not found. Cannot export.")
    except docker.errors.APIError as e:
        print(f"An error occurred: {e}")


def restart_container(client, container_name):
    try:
        container = client.containers.get(container_name)
        container.restart()
        print(f"Container {container_name} restarted successfully.")
    except docker.errors.NotFound:
        print(f"Container {container_name} not found.")
    except docker.errors.APIError as e:
        print(f"An error occurred while restarting the container: {e}")


def import_database(client, container_name, import_path, port):
    print(f"Importing database from {import_path} to container {container_name}...")

    try:
        # Check if the container already exists and remove it if it does
        container = client.containers.get(container_name)
        print(f"Container {container_name} already exists. Stopping and removing it to perform the import...")
        container.stop()
        container.remove()
        print(f"Container {container_name} removed.")
    except docker.errors.NotFound:
        print(f"Container {container_name} not found. Proceeding to create a new one...")

    # Create a new container for importing the database
    try:
        container = client.containers.run(
            'neo4j:latest',
            name=container_name,
            detach=True,
            ports={'7687/tcp': port},
            volumes={import_path: {'bind': '/data/backup.tar', 'mode': 'rw'}},
            environment={
                'NEO4J_apoc_export_file_enabled': 'true',
                'NEO4J_apoc_import_file_enabled': 'true',
                'NEO4J_apoc_import_file_useneo4jconfig': 'true',
                'NEO4J_AUTH': 'neo4j/password',
                'NEO4J_PLUGINS': '["apoc"]'
            }
        )

        # Ensure the container is fully up and running before continuing
        if not wait_for_container(container):
            print(f"Container {container_name} did not start properly.")
            return

        # Ensure the directory for the import exists
        result = container.exec_run('mkdir -p /data/backup_dir')
        if result.exit_code != 0:
            print(f"Failed to create directory: {result.output.decode('utf-8')}")
            return

        # Unpack the initial tarball
        result = container.exec_run('tar -xvf /data/backup.tar -C /data/backup_dir')
        if result.exit_code != 0:
            print(f"Failed to unpack the tarball: {result.output.decode('utf-8')}")
            return

        # Now unpack the nested tarball (actual database files)
        result = container.exec_run('tar -xvf /data/backup_dir/backup.dump.tar -C /data/backup_dir')
        if result.exit_code != 0:
            print(f"Failed to unpack the nested tarball: {result.output.decode('utf-8')}")
            return

        # List the contents of the directory to verify the files
        result = container.exec_run('ls -l /data/backup_dir')
        print(f"Contents of /data/backup_dir after extraction:\n{result.output.decode('utf-8')}")

        # Run the import command inside the container using --from-path and --overwrite-destination
        exit_code, output = container.exec_run(
            "bin/neo4j-admin database load neo4j --from-path=/data/backup_dir --overwrite-destination=true --verbose"
        )
        if exit_code != 0:
            print(f"Failed to import database: {output.decode('utf-8')}")
        else:
            print(f"Database imported successfully to container {container_name}")

    except docker.errors.APIError as e:
        print(f"An error occurred: {e}")
        return

    return container



def start_or_create_container(client, container_name, port):
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
            'neo4j:latest',
            name=container_name,
            detach=True,
            ports={'7687/tcp': port},
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

    for container in os.listdir(containers_dir):
        if container.endswith(".dump.tar"):
            import_path = os.path.join(containers_dir, container)
            container_name = container.replace(".dump.tar", "")
            #start_or_create_container(client, container_name, port)
            import_database(client, container_name, import_path, MEMORY_MAP[container_name])
            restart_container(client, container_name)


def create_memory_containers():
    client = docker.from_env(timeout=600)
    for container_name, port in MEMORY_MAP.items():
        try:
            print(f"Creating container {container_name} on port {port}...")
            container = client.containers.run(
                'neo4j:latest',
                name=container_name,
                detach=True,
                ports={'7687/tcp': port},
                environment={
                    'NEO4J_apoc_export_file_enabled': 'true',
                    'NEO4J_apoc_import_file_enabled': 'true',
                    'NEO4J_apoc_import_file_useneo4jconfig': 'true',
                    'NEO4J_AUTH': 'neo4j/password',
                    'NEO4J_PLUGINS': '["apoc"]'
                }
            )
            print(f"Container {container_name} created successfully.")
        except docker.errors.APIError as e:
            print(f"An error occurred while creating container {container_name}: {e}")


def export_all_containers():
    """
    Export all containers listed in the MEMORY_MAP to dump files.
    """
    containers_dir = os.path.join(base_dir, "memory_containers")

    # Ensure the containers directory exists
    os.makedirs(containers_dir, exist_ok=True)

    for container_name in MEMORY_MAP.keys():
        export_path = os.path.join(containers_dir, f"{container_name}.dump.tar")
        print(f"Exporting container {container_name}...")
        export_database(container_name, export_path)
        print(f"Export of {container_name} completed.")

    print("All containers have been exported successfully.")


if __name__ == '__main__':
    #character = 'athena01'
    #export_database(character, os.path.join(base_dir, "memory_containers", f"{character}.dump.tar"))
    #setup_memory_containers()
    #create_memory_containers()
    export_all_containers()
