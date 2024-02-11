# NIST NVD Data Collector and PostgreSQL Integration

## Overview

This project is designed to automate the collection of the full NIST National Vulnerability Database (NVD), excluding the current year's data, and integrate this data into a PostgreSQL database. It involves setting up a PostgreSQL server, creating specific tables to store NVD data, and running scripts to collect and push the data into the database. This solution is ideal for cybersecurity professionals, researchers, and IT administrators looking to analyze or leverage NVD data within a structured database environment.

## Components

- **Ansible Playbook**: Provisions a PostgreSQL server on a CentOS system, including database and user creation.
- **Python Scripts**:
  - `collect.py`: Collects NVD data (JSON format) from the NIST website, excluding the current year.
  - `push.py`: Processes and inserts the collected NVD data into the PostgreSQL database.
- **Bash Script**: Orchestrates the entire process from provisioning Ansible, setting up PostgreSQL, collecting NVD data, and populating the database.
- **SQL Scripts**: Define the schema for the PostgreSQL database, including tables for CVE details, problem types, references, descriptions, configurations, and impact scores.

## Requirements

- CentOS (The provided instructions are tailored for CentOS. Adjustments may be needed for other distributions.)
- Ansible
- PostgreSQL
- Python 3.x

## Setup and Execution

1. **Prepare Your CentOS System**:
   Ensure your system is up-to-date and has Python 3.x installed. PostgreSQL will be installed via Ansible.

2. **Install Ansible**:
   Follow the Bash script provided (`provision.sh`) to automate the installation of Ansible and other required components.

3. **Configure PostgreSQL with Ansible**:
   Use the provided Ansible playbook (`setup_postgresql.yml`) to install and configure PostgreSQL. This step includes creating the `nvd` database and the `nvd-user`.

4. **Database Schema**:
   SQL script files define the structure of tables needed to store NVD data. These scripts are automatically applied during the Ansible provisioning phase.

5. **Collect and Insert NVD Data**:
   After setting up the PostgreSQL database, the Bash script will execute `collect.py` to download NVD data and `push.py` to insert this data into the database.

6. **.gitignore Configuration**:
   Ensure the `nvd-data` folder, where NVD JSON files are stored temporarily, is included in `.gitignore` to prevent committing potentially large data files to your Git repository.

## Execution

Clone this repository:

```bash
git clone https://github.com/LittleSeneca/local-nvd.git 
```

move into the repository folder:

```bash
cd local-nvd
```

Run the `provision.sh` script from your terminal:

```bash
sudo ./provision.sh
```

This script will automate the entire process, from provisioning the PostgreSQL server to collecting and inserting NVD data into the database.

## Security Note

The default configuration allows the `nvd-user` to log in without a password for simplicity and demonstration purposes. In production environments, consider implementing stronger authentication methods and restricting network access to the database.

## Conclusion

This project streamlines the process of collecting and utilizing NVD data by integrating it into a structured PostgreSQL database, making it accessible and manageable for further analysis or integration into cybersecurity workflows.