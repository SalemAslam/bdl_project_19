from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import FloatType
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml import Pipeline
import os
import pandas as pd
import pickle
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from kaggle.api.kaggle_api_extended import KaggleApi
from sklearn.model_selection import train_test_split

def download_data_task(**kwargs):
  """Downloads the Telco customer churn dataset from Kaggle."""

  # Authenticate with Kaggle
  api = KaggleApi()
  api.authenticate()

  # Download the dataset
  dataset = 'blastchar/telco-customer-churn'
  api.dataset_download_files(dataset, path='.', unzip=True)

  # Set the downloaded file path as a task output (downloaded file is named 'WA_Fn-UseC_-Telco-Customer-Churn.csv')
  kwargs['ti'].xcom_push(key='file_path', value='WA_Fn-UseC_-Telco-Customer-Churn.csv') 

def preprocess_data_task(**kwargs):
    # Initialize SparkSession
    spark = SparkSession.builder.appName("TelcoChurnPreprocessing").getOrCreate()

    # Get downloaded file path from XCom
    file_path = kwargs['ti'].xcom_pull(key='file_path', task_ids='download_data')

    # Load data
    telco_data = spark.read.csv(file_path, header=True, inferSchema=True)

    # Convert TotalCharges to float and handle missing values
    telco_data = telco_data.withColumn("TotalCharges", F.col("TotalCharges").cast(FloatType()))
    telco_data = telco_data.dropna(subset=["TotalCharges"])

    # Create tenure groups
    telco_data = telco_data.withColumn("tenure_group", 
                                        F.when(F.col("tenure").between(1, 12), "1-12")
                                        .when(F.col("tenure").between(13, 24), "13-24")
                                        .when(F.col("tenure").between(25, 36), "25-36")
                                        .when(F.col("tenure").between(37, 48), "37-48")
                                        .when(F.col("tenure").between(49, 60), "49-60")
                                        .otherwise("61-72"))

    # Drop unnecessary columns
    telco_data = telco_data.drop("customerID", "tenure")

    # Convert target variable 'Churn' to binary numeric variable
    telco_data = telco_data.withColumn("Churn", F.when(F.col("Churn") == "Yes", 1).otherwise(0))

    # Convert categorical variables to dummy variables
    categorical_cols = [col for col, dtype in telco_data.dtypes if dtype == 'string']
    indexers = [StringIndexer(inputCol=column, outputCol=column+"_index") for column in categorical_cols]
    pipeline = Pipeline(stages=indexers)
    telco_data = pipeline.fit(telco_data).transform(telco_data)

    # Drop original categorical columns
    telco_data = telco_data.drop(*categorical_cols)

    # Set the final Spark DataFrame as a task output
    kwargs['ti'].xcom_push(key='telco_data', value=telco_data)

def train_model_task(**kwargs):
    # Load final data from XCom
    final_data = kwargs['ti'].xcom_pull(key='final_data', task_ids='preprocess_data')

    # Convert Spark DataFrame to Pandas DataFrame for scikit-learn
    final_data_pd = final_data.toPandas()

    # Separate features and target variable
    X = final_data_pd.drop('Churn', axis=1)
    y = final_data_pd['Churn']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define and train the DecisionTreeClassifier model
    model_dt = DecisionTreeClassifier(criterion="gini", random_state=100, max_depth=6, min_samples_leaf=8)
    model_dt.fit(X_train, y_train)

    # Save the trained model using pickle (replace if needed)
    with open('decision_tree_model_airflow.pkl', 'wb') as f:
        pickle.dump(model_dt, f)

    # Set model metrics or any output as task output (optional)
    # kwargs['ti'].xcom_push(key='model_metrics', value=model_metrics)
