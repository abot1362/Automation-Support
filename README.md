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

# Unified Infrastructure Management Platform

Welcome to the Unified Infrastructure Management Platform, a modern, smart, and multi-vendor solution for managing your entire IT infrastructure. This project provides a single pane of glass for managing network devices, virtualization platforms, security gateways, communication systems, and video surveillance, all powered by a robust backend and a powerful AI assistant.

![Platform Architecture](https://i.imgur.com/example.png) <!-- شما می‌توانید یک دیاگرام از معماری خود اینجا قرار دهید -->

##  Architectural Overview

This project follows a modern, decoupled architecture:
-   **Backend:** A powerful, asynchronous API built with **FastAPI (Python)**. It serves as the brain of the platform, handling all logic, device communication, and database interactions.
-   **Admin Frontend:** A feature-rich Single-Page Application (SPA) and Progressive Web App (PWA) built with **Next.js (React)** for administrators.
-   **User Frontend:** A mobile-first, installable PWA, also built with **Next.js**, providing end-users with access to services like support tickets and remote access.

---

## 🚀 Getting Started: Local Development Setup

This guide will walk you through setting up the entire platform for local development.

### Prerequisites

-   **Node.js** (v18 or later)
-   **Python** (v3.9 or later)
-   **MariaDB** (or MySQL) database server installed and running.
-   `git` for cloning the repository.

### Step 1: Clone the Repository

```bash
git clone https://github.com/abot1362/Automation-Support
cd Automation-Support


