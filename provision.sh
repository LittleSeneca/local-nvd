#!/bin/bash

# Step 1: Install Ansible
echo "Installing Ansible..."
sudo yum install -y epel-release
sudo yum install -y ansible

# Verify Ansible installation
ansible --version

# Step 2: Run Ansible Playbook to Set Up PostgreSQL
echo "Running Ansible Playbook to set up PostgreSQL..."
# Replace 'setup_postgresql_local_centos.yml' with the path to your Ansible playbook
ansible-playbook setup_postgresql_local_centos.yml

# Check if the playbook execution was successful
if [ $? -ne 0 ]; then
    echo "Ansible playbook execution failed."
    exit 1
fi

# Step 3: Run collect.py Python Script
echo "Running collect.py..."
# Replace './collect.py' with the actual path to your collect.py script
python ./collect.py

# Check if the script execution was successful
if [ $? -ne 0 ]; then
    echo "Execution of collect.py failed."
    exit 1
fi

# Step 4: Run push.py Python Script
echo "Running push.py..."
# Replace './push.py' with the actual path to your push.py script
python ./push.py

# Check if the script execution was successful
if [ $? -ne 0 ]; then
    echo "Execution of push.py failed."
    exit 1
fi

echo "Provisioning and script execution completed successfully."
