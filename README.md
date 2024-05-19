# Telco Customer Churn Prediction ML pipeline

## Project Overview

This project aims to predict customer churn for a telecommunications company using machine learning. It includes a complete pipeline from data downloading, preprocessing, model training, and deployment of a REST API for predictions. Additionally, it includes monitoring with Prometheus and a machine learning experiment tracking with MLflow.

## Directory Structure

```
├── main_files
│   ├── app-main.py
│   ├── app-client.py
│   ├── decision_tree_model.pkl
│   ├── json_test_data.json
│   ├── mlflow.ipynb
│   ├── prometheus.yml
│   ├── requirements.txt
│   ├── Dockerfile
├── dag
│   ├── airflow.py
│   ├── airflow_functions.py
│   ├── WA_Fn-UseC_-Telco-Customer-Churn.csv
└── README.md
```

## Setup and Installation

### Prerequisites

- Python 3.10.4
- Docker
- Airflow
- Prometheus
- MLflow
- ApacheSpark

### Clone the Repository

```bash
git clone https://github.com/yourusername/telco-churn-prediction.git
cd telco-churn-prediction
```

### Install Python Dependencies

1. **Install dependencies for the main application:**

   ```bash
   cd main_files
   pip install -r requirements.txt
   ```

2. **Airflow dependencies:**

   ```bash
   pip install apache-airflow
   pip install kaggle
   ```

### Running the Application

1. **Start the Flask API:**

   If not using Docker, you can run the Flask app directly:

   ```bash
   cd main_files
   python app-main.py
   ```

2. **Send a test prediction request:**

   ```bash
   cd main_files
   python app-client.py
   ```

### MLflow Setup

1. **Run the MLflow notebook:**

   Open `mlflow.ipynb` in Jupyter Notebook or Jupyter Lab and run all the cells to train and log different models. Make sure you have MLflow installed and started:

   Access the MLflow UI at `http://localhost:5000`.

## Reproducing the Results

1. **Data Download and Preprocessing:**

   Use Airflow to download and preprocess the data. Trigger the DAG from the Airflow UI.

2. **Model Training:**

   Use the MLflow notebook `mlflow.ipynb` to train and log the models.

3. **Deploy and Test the API:**

   Deploy the Flask app using Docker or directly on your local machine. Use `app-client.py` to test the API endpoints.

4. **Monitoring:**

   Set up Prometheus to monitor the API metrics as configured in `prometheus.yml`.

## Project Components

### 1. `main_files/`
- **app-main.py:** The main Flask application file for serving the model and handling requests.
- **app-client.py:** A client script to test the API by sending sample requests.
- **decision_tree_model.pkl:** The trained Decision Tree model file.
- **json_test_data.json:** Sample JSON data for testing the API.
- **mlflow.ipynb:** Jupyter notebook for training models and logging experiments with MLflow.
- **prometheus.yml:** Configuration file for Prometheus to monitor the Flask API.
- **requirements.txt:** Python dependencies for the main application.
- **Dockerfile:** Docker configuration to containerize the Flask application.

### 2. `dag/`
- **airflow.py:** Airflow DAG definition for the data preprocessing and model training pipeline.
- **airflow_functions.py:** Python functions used in the Airflow DAG.
- **WA_Fn-UseC_-Telco-Customer-Churn.csv:** The dataset used for training and testing.

### Airflow Setup

1. **Initialize Airflow:**

   ```bash
   airflow db init
   ```

2. **Create a new DAG file:**

   Copy the `airflow.py` and `airflow_functions.py` files to your Airflow DAGs directory (typically `~/airflow/dags`).

3. **Start the Airflow web server and scheduler:**

   ```bash
   airflow webserver
   airflow scheduler
   ```

4. **Access Airflow UI:**

   Open your browser and go to `http://localhost:8080` to access the Airflow UI. Trigger the `telco_churn_preprocessing` DAG to start the pipeline.

### Prometheus Setup

1. **Run Prometheus:**

   ```bash
   prometheus --config.file=main_files/prometheus.yml
   ```

### Docker Setup

1. **Build the Docker image:**

   ```bash
   cd main_files
   docker build -t telco-churn-app .
   ```

2. **Run the Docker container:**

   ```bash
   docker run -p 5000:5000 telco-churn-app
   ```

## Notes

- Make sure to set up your Kaggle API credentials before running the Airflow pipeline.
- Adjust paths and configurations as needed based on your environment.
- Ensure Docker and all other dependencies are properly installed and running.

## Author

Salem Aslam
