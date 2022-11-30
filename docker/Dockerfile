FROM python:3.10-alpine

### -------------------------------------------------
### Metadata information
### -------------------------------------------------
LABEL name="ansible-deploy-vmseries"
LABEL maintainer="cremsburg.dev@gmail.com"
LABEL description="Ansible container to deploy VM series firewalls on VMware"
LABEL license="Apache 2.0"
LABEL url="https://github.com/cdot65/ansible-deploy-vmseries"
LABEL build-date="20221130"


# ---------------------------------------------------------------------------
# Change directory to /home/ansible
# ---------------------------------------------------------------------------
WORKDIR /home/ansible

# ---------------------------------------------------------------------------
# Add and install python packages
# ---------------------------------------------------------------------------
ADD docker/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ---------------------------------------------------------------------------
# Install Ansible Galaxy roles and collections
# ---------------------------------------------------------------------------
RUN ansible-galaxy collection install paloaltonetworks.panos
RUN ansible-galaxy collection install community.vmware

# ---------------------------------------------------------------------------
# COPY FILES TO CONTAINER IMAGE
# ---------------------------------------------------------------------------
COPY docker/ansible.cfg /etc/ansible/ansible.cfg
COPY ansible/inventory.yaml inventory.yaml
COPY ansible/deploy.vmseries.yaml deploy.vmseries.yaml

### ---------------------------------------------------------------------------
### Environmentals
### ---------------------------------------------------------------------------
ENV ANSIBLE_CONFIG /etc/ansible/ansible.cfg
