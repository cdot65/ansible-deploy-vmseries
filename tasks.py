"""Tasks for use with Invoke."""

import os
import logging
from invoke import task
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# DOCKER PARAMETERS
# ---------------------------------------------------------------------------
DOCKER_IMG = "ghcr.io/cdot65/ansible-deploy-vmseries"
DOCKER_TAG = "0.0.1"

# ---------------------------------------------------------------------------
# SYSTEM PARAMETERS
# ---------------------------------------------------------------------------
PWD = os.getcwd()

# ---------------------------------------------------------------------------
# ANSIBLE ARGUMENTS AND COMMANDS
# ---------------------------------------------------------------------------
load_dotenv("ansible/.env")

VCENTER_HOSTNAME = os.environ.get("VCENTER_HOSTNAME", "my-vcenter")
VCENTER_USERNAME = os.environ.get("VCENTER_USERNAME", "my-username")
VCENTER_PASSWORD = os.environ.get("VCENTER_PASSWORD", "my-password")
VCENTER_DATACENTER = os.environ.get("VCENTER_DATACENTER", "my-datacenter")
VCENTER_FOLDER = os.environ.get("VCENTER_FOLDER", "/Templates")
VCENTER_TEMPLATE = os.environ.get("VCENTER_TEMPLATE", "vmseries-template")
VCENTER_ESXI_HOST = os.environ.get("VCENTER_ESXI_HOST", "my-esx-server")

VM_NAME = "vmseries-1"


# ---------------------------------------------------------------------------
# LOGGING PARAMETERS
# ---------------------------------------------------------------------------
logger = logging.getLogger()
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
log_format = "%(asctime)s | %(levelname)s: %(message)s"
console_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(console_handler)


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------
def console_msg(message):
    """Provide a little formatting help for console messages."""
    logger.info(message)


def run_command(context, command, **kwargs):
    """Helper function to run commands based on arguments."""
    context.run(command, **kwargs)


# ---------------------------------------------------------------------------
# ANSIBLE CONTAINER IMAGE BUILD
# ---------------------------------------------------------------------------
@task(
    help={
        "force_rm": "Always remove existing containers.",
        "cache": "Determine whether or not to use local cache.",
    }
)
def build(context, force_rm=False, cache=True):
    """Build our Ansible docker container image.
    Args:
        context (obj): Used to run specific commands
        force_rm (Bool): will remove any local instance [default: False]
        cache (Bool): determine whether or not to use cache [default: True]
    """

    # build command pointing to a folder outside our local context
    command = "docker build -f docker/Dockerfile"

    if not cache:
        command += " --no-cache"
    if force_rm:
        command += " --force-rm"

    # tokens used by our app are passed into the container build process
    # ansible_username = f"ANSIBLE_NET_USERNAME={VCENTER_USERNAME}"
    # ansible_password = f"ANSIBLE_NET_PASSWORD={VCENTER_PASSWORD}"

    # build arguments pass our tokens into the build process
    # ansible_args = f"--build-arg={ansible_username} --build-arg={ansible_password}"

    console_msg(f"Building our Docker container image {DOCKER_IMG}:{DOCKER_TAG}")
    context.run(
        f"{command} -t {DOCKER_IMG}:{DOCKER_TAG} .",
    )


# ---------------------------------------------------------------------------
# DOCKER CONTAINER SHELL
# ---------------------------------------------------------------------------
@task
def shell(context):
    # Get access to the BASH shell within our container
    print("Jumping into container, type exit to return to host")
    context.run(
        f"docker run -it --rm \
            {DOCKER_IMG}:{DOCKER_TAG} /bin/sh",
        pty=True,
    )


# ---------------------------------------------------------------------------
# EXECUTE PLAYBOOK FROM WITHIN CONTAINER
# ---------------------------------------------------------------------------
@task
def ansible(context):
    # Execute Ansible playbook from within the container
    context.run(
        f"docker run -it \
            --rm \
            {DOCKER_IMG}:{DOCKER_TAG} ansible-playbook -vvv deploy.vmseries.yaml \
            -e vcenter_hostname='{VCENTER_HOSTNAME}' \
            -e vcenter_username='{VCENTER_USERNAME}' \
            -e vcenter_password='{VCENTER_PASSWORD}' \
            -e datacenter='{VCENTER_DATACENTER}' \
            -e folder='{VCENTER_FOLDER}' \
            -e template='{VCENTER_TEMPLATE}' \
            -e esxi_host='{VCENTER_ESXI_HOST}' \
            -e vm_name='{VM_NAME}'",
        pty=True,
    )
