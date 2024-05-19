from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from airflow_functions import download_data_task, preprocess_data_task, train_model_task

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 14),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

# Define the DAG with its parameters
dag = DAG(
    'telco_churn_preprocessing', 
    description='A DAG to download, preprocess data and train model',  # Description of the DAG
    default_args=default_args, 
    schedule=None,  # Schedule for the DAG, set to None for manual triggering
    )

download_data_task = PythonOperator(
    task_id='download_data',
    python_callable=download_data_task,
    provide_context=True,
    dag=dag
)

preprocess_data_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data_task,
    provide_context=True,
    dag=dag
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model_task,
    provide_context=True,
    dag=dag
)

# Set dependencies between tasks
download_data_task >> preprocess_data_task >> train_model_task