Developing an Integrated Platform for Different Network Devices

Overview

This project is a Django-based web application designed to provide a centralized platform for managing and monitoring various network devices. It allows users to configure settings, analyze network data, and interact with devices seamlessly through an intuitive dashboard.

Features

Real-time Device Monitoring: Track the status and performance of connected devices.

Configuration Management: Easily update settings and firmware.

Centralized Dashboard: Access all essential network information from one interface.

Security Measures: Implements authentication and role-based access control.

Automated Network Configuration: Uses YAML-based configurations to manage network settings.

Multi-Vendor Device Support: Uses Ansible to interact with devices from different network vendors.

Installation

Prerequisites

Ensure you have the following installed on your system:

Python 3.7+

Django Framework

Required dependencies (listed in requirements.txt)

Ansible (for network automation)

Steps

Clone the Repository:

git clone https://github.com/mroy9090/Developing-an-Integrated-Platform-for-Different-Network-Devices.git
cd Developing-an-Integrated-Platform-for-Different-Network-Devices

Create a Virtual Environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies:

pip install -r requirements.txt

Apply Database Migrations:

python manage.py migrate

Run the Server:

python manage.py runserver

Access the Application:
Open your browser and go to http://127.0.0.1:8000/.

Project Structure

Developing-an-Integrated-Platform/
│-- admin_pannel/          # Django settings, URLs, and WSGI
│-- dashboard/             # Main application logic and views
│-- static/                # Static assets like CSS, JS, images
│-- templates/             # HTML templates for frontend
│-- ipaddress.yml          # Network configuration file
│-- yml.py                 # Script for processing YAML configurations
│-- db.sqlite3             # SQLite database
│-- manage.py              # Django management script
│-- __pycache__/           # Compiled Python files

Configuration Management

ipaddress.yml: Stores network device configurations and credentials.

yml.py: Parses YAML files and applies settings using Ansible.

Django Admin Panel: Available at /admin for managing users and settings.

Ansible Integration for Multi-Vendor Network Devices

This project leverages Ansible to automate network device configurations across different vendors. The automation process includes:

Device Connectivity: Uses Ansible modules to establish SSH connections to routers, switches, and firewalls.

Configuration Deployment: Applies YAML-based configurations to update device settings.

Vendor-Agnostic Approach: Works with Cisco, Juniper, Arista, and other network devices.

Playbook Execution: Run Ansible playbooks to configure multiple devices simultaneously:

ansible-playbook playbook.yml

Usage

Login as Admin: Access the admin panel at /admin to manage users and settings.

Device Management: View, add, or modify network devices via the dashboard.

Automated Configuration: Run yml.py to process YAML configurations:

python yml.py

Execute Ansible Playbooks: Use Ansible to push configurations to multiple devices.

Contribution

Contributions are welcome! Follow these steps:

Fork the repository.

Create a new branch (feature-branch-name).

Make your changes and commit (git commit -m 'Description of changes').

Push to the branch (git push origin feature-branch-name).

Submit a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Contact

For any issues or contributions, feel free to reach out via GitHub Issues.
