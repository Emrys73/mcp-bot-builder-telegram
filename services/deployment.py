"""Docker deployment service for bots."""

import docker
from pathlib import Path
from typing import Optional
import logging

from config import BOTS_DIR, DOCKER_NETWORK

logger = logging.getLogger(__name__)


class DeploymentService:
    """Manages Docker deployment of bots."""
    
    def __init__(self):
        try:
            self.client = docker.from_env()
            self._ensure_network()
        except docker.errors.DockerException as e:
            logger.error(f"Failed to connect to Docker: {e}")
            raise
    
    def _ensure_network(self):
        """Ensure Docker network exists."""
        try:
            self.client.networks.get(DOCKER_NETWORK)
        except docker.errors.NotFound:
            self.client.networks.create(
                DOCKER_NETWORK,
                driver="bridge"
            )
    
    def build_image(self, bot_name: str, bot_dir: Path) -> Optional[str]:
        """Build Docker image for a bot."""
        try:
            image_tag = f"botbuilder-{bot_name}:latest"
            
            logger.info(f"Building Docker image for {bot_name}...")
            image, build_logs = self.client.images.build(
                path=str(bot_dir),
                tag=image_tag,
                rm=True,
                forcerm=True
            )
            
            logger.info(f"Successfully built image {image_tag}")
            return image_tag
        except docker.errors.BuildError as e:
            logger.error(f"Build failed for {bot_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error building {bot_name}: {e}")
            return None
    
    def create_container(
        self,
        bot_name: str,
        image_tag: str,
        bot_token: str,
        env_vars: Optional[dict] = None
    ) -> Optional[str]:
        """Create Docker container for a bot."""
        try:
            container_name = f"botbuilder-{bot_name}"
            
            # Prepare environment variables
            environment = {
                "BOT_TOKEN": bot_token,
            }
            if env_vars:
                environment.update(env_vars)
            
            # Check if container already exists
            try:
                existing = self.client.containers.get(container_name)
                existing.remove(force=True)
            except docker.errors.NotFound:
                pass
            
            logger.info(f"Creating container {container_name}...")
            container = self.client.containers.create(
                image=image_tag,
                name=container_name,
                environment=environment,
                network=DOCKER_NETWORK,
                restart_policy={"Name": "unless-stopped"},
                detach=True
            )
            
            logger.info(f"Successfully created container {container_name}")
            return container.id
        except docker.errors.APIError as e:
            logger.error(f"Failed to create container for {bot_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating container for {bot_name}: {e}")
            return None
    
    def start_container(self, container_id: str) -> bool:
        """Start a Docker container."""
        try:
            container = self.client.containers.get(container_id)
            container.start()
            logger.info(f"Started container {container_id}")
            return True
        except docker.errors.APIError as e:
            logger.error(f"Failed to start container {container_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error starting container {container_id}: {e}")
            return False
    
    def stop_container(self, container_id: str) -> bool:
        """Stop a Docker container."""
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            logger.info(f"Stopped container {container_id}")
            return True
        except docker.errors.APIError as e:
            logger.error(f"Failed to stop container {container_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error stopping container {container_id}: {e}")
            return False
    
    def get_container_status(self, container_id: str) -> Optional[str]:
        """Get container status."""
        try:
            container = self.client.containers.get(container_id)
            return container.status
        except docker.errors.NotFound:
            return None
        except Exception as e:
            logger.error(f"Error getting container status {container_id}: {e}")
            return None
    
    def get_container_logs(self, container_id: str, tail: int = 50) -> Optional[str]:
        """Get container logs."""
        try:
            container = self.client.containers.get(container_id)
            logs = container.logs(tail=tail).decode('utf-8')
            return logs
        except docker.errors.NotFound:
            return None
        except Exception as e:
            logger.error(f"Error getting container logs {container_id}: {e}")
            return None
    
    def find_container_by_name(self, bot_name: str) -> Optional[str]:
        """Find container ID by bot name."""
        try:
            container_name = f"botbuilder-{bot_name}"
            container = self.client.containers.get(container_name)
            return container.id
        except docker.errors.NotFound:
            return None
        except Exception as e:
            logger.error(f"Error finding container for {bot_name}: {e}")
            return None
