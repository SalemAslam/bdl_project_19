import requests
import json

# Assuming the file is named "data.json" in your current directory (modify the filename if needed)
with open("json_test_data.json", "r") as f:
  json_entries = json.load(f)

api_url = "http://localhost:5000/test_predict"

#json data entry example
# data = {
#   "SeniorCitizen": 0,
#   "MonthlyCharges": 29.85,
#   "TotalCharges": 29.85,
#   "gender_index": 1,
#   "Partner_index": 1,
#   "Dependents_index": 0,
#   "PhoneService_index": 1,
#   "MultipleLines_index": 0,
#   "InternetService_index": 1,
#   "OnlineSecurity_index": 0,
#   "OnlineBackup_index": 0,
#   "DeviceProtection_index": 0,
#   "TechSupport_index": 0,
#   "StreamingTV_index": 0,
#   "StreamingMovies_index": 0,
#   "Contract_index": 0,
#   "PaperlessBilling_index": 1,
#   "PaymentMethod_index": 3,
#   "tenure_group_index": 0
# }

headers = {'Content-Type': 'application/json'}

# response = requests.post(api_url, json=data, headers=headers)
# print("Response status code:", response.status_code)
# print("Response content:", response.json())

n = 100 # number of datapoints to be run on the API '/test_predict' endpoint
for entry in json_entries[:n]:
  response = requests.post(api_url, json=entry, headers=headers)
  print("Response status code:", response.status_code)
  print("Response content:", response.json())
  print("---")  # Separator between entries

print("All entries processed!")