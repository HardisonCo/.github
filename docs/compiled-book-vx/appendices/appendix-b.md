# Installation & Setup Guide

Detailed instructions for installing and setting up the HMS development environment.

## System Requirements

- Node.js 16 or higher
- Python 3.8 or higher
- Docker (for containerized deployment)
- 8GB RAM minimum, 16GB recommended
- 50GB disk space

## Installation Steps

### 1. Clone the Repository

```bash


git clone https://github.com/yourusername/hms-framework.git
cd hms-framework


```text

### 2. Install Dependencies

```bash


## Install Node.js dependencies
npm install

## Install Python dependencies
pip install -r requirements.txt


```text

### 3. Configure Environment

```bash


## Copy example environment file
cp .env.example .env

## Edit .env file with your settings
nano .env


```text

### 4. Start Development Server

```bash


npm run dev


```text

## Troubleshooting

If you encounter any issues during installation, please refer to the following resources:

- Check the logs in the `logs` directory
- Consult the online documentation at https://docs.hms-framework.org
- Join our community Discord server for real-time help

```text

