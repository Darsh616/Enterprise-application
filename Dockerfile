# Step 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Install system dependencies for MySQL and build tools
RUN apt-get update && \
    apt-get install -y pkg-config libmariadb-dev build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Step 4: Copy the current directory contents into the container at /app
COPY . /app

# Step 5: Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Envirnoment vairables 
ENV MYSQL_HOST darshan.cj4oqcie8m6x.ap-south-1.rds.amazonaws.com
ENV MYSQL_USER admin
ENV MYSQL_PASSWORD Local_1234567
ENV MYSQL_DB darshan

# Step 6: Run the Flask app using Gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000","--workers", "2", "--timeout", "120"]

# Expose port for the Flask app
EXPOSE 5000
