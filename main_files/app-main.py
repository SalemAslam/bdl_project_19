from flask import Flask, request, jsonify, Response
import pandas as pd
import joblib
import prometheus_client
from prometheus_client import start_http_server, Counter, Histogram, Gauge
import time
import psutil  # Import psutil
import threading



app = Flask(__name__)

# Load the trained model
model = joblib.load('decision_tree_model.pkl')

# Define Prometheus metrics
REQUESTS = Counter('http_requests_total', 'Total HTTP Requests')
run_time = Gauge("API_runtime", "Time taken for inference in seconds")
CLIENT_IP_REQUESTS = Counter('http_requests_client_ip_total', 'Total HTTP Requests per Client IP', ['client_ip'])
REQUEST_SIZE = Gauge('http_request_size', 'Size of HTTP Request')
PROCESSING_TIME_PER_CHAR = Gauge('http_processing_time_per_char_microseconds', 'Processing time per character in microseconds')

memory_utilization = Gauge("API_memory_utilization", "API memory utilization in percent")
cpu_utilization = Gauge("API_cpu_utilization", "API CPU utilization in percent")

@app.route('/')
def home():
    return "Welcome to the Telco Churn Prediction RestAPI!"

@app.route('/predict', methods=['POST'])
def predict():
    start_time = time.time()

    REQUESTS.inc()  # Increment total requests counter
    client_ip = request.remote_addr
    CLIENT_IP_REQUESTS.labels(client_ip).inc()

    data = request.get_json(force=True)
    input_length = len(str(data))
    REQUEST_SIZE.set(input_length)
    
    data_df = pd.DataFrame([data])
    
    # Assuming that the incoming data is already in the same format as the trained model
    prediction = model.predict(data_df)
    prediction_proba = model.predict_proba(data_df)

    end_time = time.time()
    inference_time = end_time - start_time
    run_time.set(inference_time)

    total_time = (time.time() - start_time) * 1e6  # Convert to microseconds
    processing_time_per_char = total_time / input_length
    PROCESSING_TIME_PER_CHAR.set(processing_time_per_char)

    result = {
        'prediction': int(prediction[0]),
        'probability(not churn, churn)': prediction_proba[0].tolist()
    }

    return jsonify(result)

@app.route('/test_predict', methods=['POST'])
def test_predict():

    REQUESTS.inc()  # Increment total requests counter
    client_ip = request.remote_addr
    CLIENT_IP_REQUESTS.labels(client_ip).inc()

    try:
        start_time = time.time()

        data = request.get_json(force=True)
        input_length = len(str(data))
        REQUEST_SIZE.set(input_length)
        
        data_df = pd.DataFrame([data])
        
        prediction = model.predict(data_df)
        prediction_proba = model.predict_proba(data_df)

        total_time = (time.time() - start_time) * 1e6  # Convert to microseconds
        processing_time_per_char = total_time / input_length
        PROCESSING_TIME_PER_CHAR.set(processing_time_per_char)

        result = {
            'prediction': int(prediction[0]),
            'probability(not churn, churn)': prediction_proba[0].tolist()
        }
        
        end_time = time.time()
        inference_time = end_time - start_time
        run_time.set(inference_time)

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Internal Server Error

# Endpoint to expose Prometheus metrics
@app.route('/metrics')
def metrics():
    return Response(prometheus_client.generate_latest(), mimetype="text/plain")

def update_metrics():
    while True:
        memory_utilization.set(psutil.virtual_memory().percent)
        cpu_utilization.set(psutil.cpu_percent(interval=1))
        time.sleep(1)  # Update every second

if __name__ == '__main__':
    metrics_thread = threading.Thread(target=update_metrics)
    metrics_thread.start()
    app.run(debug=True)

