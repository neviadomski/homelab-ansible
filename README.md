# Project Summary

This project is an Ansible playbook that automates the configuration and management of a HomeLab environment. It provides a set of roles that can be used to deploy and manage various services and applications.

## User Roles

The following user roles are available in this project:

1. `build_rhel_template`: This role is used to build a Red Hat Enterprise Linux (RHEL) template for virtual machine provisioning.

2. `create_rhel_template`: This role is used to create a new virtual machine from the RHEL template.

## Usage Instructions

To use this project, follow these steps:

1. Clone the repository to your local machine.

2. Install Ansible on your system if you haven't already.

3. Navigate to the project directory.

4. Edit the `inventory.yml` file to specify the target hosts and their corresponding roles.

5. Run the playbook using the following command:

    ```bash
    ansible-playbook main.yaml
    ```

6. Sit back and relax while Ansible automates the deployment and configuration of your HomeLab environment.
