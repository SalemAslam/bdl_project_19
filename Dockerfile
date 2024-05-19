# Use the official Python image
FROM python:3.10.4

# Install necessary system packages
RUN apt-get update && \
    apt-get install -y libhdf5-dev pkg-config build-essential curl libssl-dev libffi-dev python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy only the specific files you want
COPY decision_tree_model.pkl /app
COPY json_test_data.json /app
COPY WA_Fn-UseC_-Telco-Customer-Churn.csv /app
COPY requirements.txt /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Set environment variables for Airflow
ENV AIRFLOW_HOME=/usr/local/airflow

# Install Airflow
RUN pip install apache-airflow==2.2.4

# Initialize the Airflow database
RUN airflow db init

# Expose ports for Flask and Airflow
EXPOSE 5000
EXPOSE 8080

# Command to run the Airflow scheduler and webserver in the background, and Flask app
CMD airflow scheduler & airflow webserver --port 8080 & python app.py
