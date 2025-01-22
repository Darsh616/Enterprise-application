# Readme For Docker compose for multi container application
# Docker Compose Setup for Flask Application and MySQL Database

This guide will help you set up a multi-container environment using Docker and Docker Compose. The environment consists of a Flask application container and a MySQL database container.

## Prerequisites

1. **Docker**: Make sure Docker is installed on your machine.
2. **Docker Compose**: Ensure that Docker Compose is installed as well.
3. **SSH/Sudo Access**: You should have proper rights to use Docker and Docker Compose commands (e.g., be part of the `docker` group or use `sudo`).

### Step 1: Install Docker

If you don’t have Docker installed, use the following commands based on your operating system.

#### On Ubuntu:

```bash
sudo apt update
sudo apt install -y docker.io
To verify the Docker installation:

bash
Copy
docker --version
If you see the version, then Docker is installed correctly.

On Windows:
Download Docker from the official Docker website and follow the installation instructions.

Step 2: Install Docker Compose
On Ubuntu:
bash
Copy
sudo apt-get install -y docker-compose
On Windows:
Docker Compose comes preinstalled with Docker Desktop.

To verify Docker Compose installation:

bash
Copy
docker-compose --version
Step 3: Prepare Your Project Directory
Ensure your project directory contains the following:

Dockerfile – to build your Flask app container.
docker-compose.yml – configuration for both the Flask app and MySQL database.
Application Files – Flask app, requirements, templates, etc.
Step 4: Create docker-compose.yml Configuration File
Create a docker-compose.yml file with the following contents:

yaml
Copy
version: '3.8'

services:
  flask-app:
    image: flask.app
    build: .
    networks:
      - mynetwork
    ports:
      - "5000:5000"
    environment:
      - RDS_HOST=mysql-db
      - RDS_PORT=3306
      - RDS_USER=root
      - RDS_PASSWORD=my-secret-pw
      - RDS_DB_NAME=mydb

  mysql-db:
    image: mysql:latest
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
      MYSQL_DATABASE: mydb
    networks:
      - mynetwork
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql

networks:
  mynetwork:
    driver: bridge

volumes:
  mysql-data:
    driver: local
flask-app: This container runs your Flask application.
mysql-db: This container runs a MySQL database.
Network Configuration: Both containers will communicate via the custom network mynetwork.
Step 5: Build Your Flask App Image
Make sure that your Flask application has a Dockerfile for building the container. Here’s an example of a simple Dockerfile for Flask:

Dockerfile
Copy
# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files to container
COPY . /app/

# Expose the Flask app port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
requirements.txt: This file should contain all the dependencies for your Flask app, such as:
txt
Copy
Flask
mysql-connector-python
Step 6: Set Proper Docker Permissions
If you’re running into permission issues with Docker, ensure that your user is part of the docker group to avoid needing sudo for Docker commands.

To add your user to the docker group:

bash
Copy
sudo usermod -aG docker $USER
After running this command, log out and log back in or restart your machine for the changes to take effect.
Step 7: Build and Run Containers with Docker Compose
Build the Containers:

In the project directory (where the docker-compose.yml is located), run:

bash
Copy
docker-compose up --build
This will build both the Flask app and MySQL database containers and start them.

Run Containers in Detached Mode (Optional):

If you want to run containers in the background:

bash
Copy
docker-compose up -d --build
Check the Logs:

You can check the logs for both services using:

bash
Copy
docker-compose logs flask-app
docker-compose logs mysql-db
Step 8: Access the Application
Once the containers are up and running, you can access your Flask application by visiting:

bash
Copy
http://localhost:5000
Step 9: Stopping the Containers
When you’re done with the containers, stop them with:

bash
Copy
docker-compose down
This will stop and remove all running containers.

Troubleshooting
1. Permission Denied Error
If you encounter a permission denied error when trying to run Docker commands, it usually means that your user does not have the necessary privileges to run Docker commands. You can fix this by adding your user to the Docker group (as described in Step 6).

2. MySQL Database Connection Issues
Make sure the environment variables (such as RDS_HOST, RDS_PORT, etc.) in your Flask app container are correctly set to match the MySQL container's details.

For example:

RDS_HOST should be set to mysql-db (the name of the MySQL container in the Docker Compose file).
RDS_PORT should be 3306.
If you’re using AWS RDS instead of the local MySQL container, adjust the connection details in your Flask app.

3. Accessing MySQL from Flask
Ensure your Flask app is correctly using the MySQL connection details to connect to the database. Here is an example of connecting from Flask to MySQL:

python
Copy
import mysql.connector

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host="mysql-db",  # or your RDS endpoint
    user="root",
    password="my-secret-pw",
    database="mydb"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM your_table")
Step 10: Clean Up
To remove all containers, volumes, and networks used by Docker Compose, use:

bash
Copy
docker-compose down -v
This will clean up your environment.
