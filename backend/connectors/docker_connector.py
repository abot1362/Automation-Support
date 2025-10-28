# connectors/docker_connector.py

import docker
from docker.tls import TLSConfig
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
import logging

def get_docker_client(db: Session, host_id: int):
    """
    Initializes and returns a Docker client connected to a specific Docker host.
    """
    host = db.query(models.DockerHost).filter(models.DockerHost.id == host_id).first()
    if not host:
        raise HTTPException(status_code=404, detail="Docker host not found.")

    try:
        tls_config = None
        # If TLS paths are provided in the DB, configure TLS for a secure connection
        if host.tls_cert_path and host.tls_key_path:
            tls_config = TLSConfig(
                client_cert=(host.tls_cert_path, host.tls_key_path),
                # You might also need ca_cert and to set verify=True
                verify=False 
            )
        
        client = docker.DockerClient(base_url=host.docker_url, tls=tls_config)
        
        # Test the connection
        if not client.ping():
            raise Exception("Docker daemon is not responding.")
        
        logging.info(f"Successfully connected to Docker host '{host.name}'.")
        return client

    except docker.errors.DockerException as e:
        logging.error(f"Docker connection to '{host.name}' failed: {e}")
        raise HTTPException(status_code=500, detail=f"Docker connection failed: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while connecting to Docker host '{host.name}': {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
