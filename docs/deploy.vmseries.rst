=======================
pb.deploy.vmseries.yaml
=======================

-------------------------------------------
deploy a virtual firewall on VMware vCenter
-------------------------------------------

deploy.vmseries
===============

This module will deploy a vmseries on VMware vCenter

Example
-------

Here is a basic example of using the module to deploy a vmseries.

You'll need to pass in some parameters, as shown below

.. code-block:: yaml

    ---
    ### ---------------------------------------------------------------------------
    ### DEPLOY vmseries
    ### ---------------------------------------------------------------------------
    - hosts: "localhost"
      connection: local
      gather_facts: False
      become: False
      tasks:

        - name: "### CLONE A vmseries ###"
          community.vmware.vmware_guest:
            hostname: "{{ vcenter_hostname }}"
            username: "{{ vcenter_username }}"
            password: "{{ vcenter_password }}"
            datacenter: "{{ datacenter }}"
            state: present
            folder: "{{ folder }}"
            template: "{{ template }}"
            name: "{{ vm_name }}"
            esxi_hostname: "{{ esxi_host }}"
            wait_for_ip_address: True
            validate_certs: False
          delegate_to: localhost
          register: vmseries_details
