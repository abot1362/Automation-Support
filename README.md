# Unified Infrastructure Management Platform

This is the central repository for the Unified Infrastructure Management Platform, a multi-vendor solution for managing network and IT infrastructure.

## Project Overview

This platform provides a single pane of glass for managing:
- Network Devices (MikroTik, Cisco)
- Security Gateways (FortiGate)
- Wireless Infrastructure (UniFi)
- Virtualization (VMware, Proxmox, Docker)
- Communications (Asterisk, FreeSWITCH)
- Video Surveillance (Hikvision, Shinobi, etc.)

## Getting Started

### Prerequisites
- Python 3.9+
- MariaDB (or MySQL)
- Nginx (for production)
- An account with a DNS provider like Cloudflare for SSL (optional but recommended)

### Installation
1.  **Clone the repository:**
    ```bash
    git clone [your-repo-url]
    cd [your-repo-name]
    ```
2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure the environment:**
    - Copy `.env.example` to `.env`.
    - Edit the `.env` file with your database credentials, secret keys, and API keys.
5.  **Setup the database:**
    - Ensure your MariaDB server is running.
    - Create the database and user as specified in your `.env` file.
    - Run the database migrations:
        ```bash
        # First time setup
        alembic init alembic
        # Then configure alembic.ini and alembic/env.py
        
        # Create and apply migrations
        alembic revision --autogenerate -m "Initial migration"
        alembic upgrade head
        ```
6.  **Run the application (for development):**
    ```bash
    uvicorn main:app --reload
    ```
The application will be available at `http://127.0.0.1:8000`.
