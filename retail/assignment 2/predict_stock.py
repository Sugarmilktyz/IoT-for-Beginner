import requests
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# === 1. Select image from computer ===
Tk().withdraw()
image_path = askopenfilename(title="Select an image to detect objects")

if not image_path:
    print("No image selected. Exiting program.")
    exit()

# === 2. Prediction Key and Endpoint from Custom Vision ===
prediction_key = "3hmoF5zXHEAtZqqwNc89URoPbYWVXGeRcA61Iq6fZF7hPWb1ry7hJQQJ99BGACYeBjFXJ3w3AAAIACOGKFPH"
prediction_endpoint = "https://stock-detector-prediction1.cognitiveservices.azure.com/customvision/v3.0/Prediction/d64f1f3b-2a63-48c8-b289-64872e5fdcde/detect/iterations/Iteration1/image"

# === 3. Read image and send to Prediction API ===
with open(image_path, "rb") as image_file:
    image_data = image_file.read()

headers = {
    "Prediction-Key": prediction_key,
    "Content-Type": "application/octet-stream"
}

response = requests.post(prediction_endpoint, headers=headers, data=image_data)

# === 4. Handle the result ===
if response.status_code != 200:
    print("Error when sending request:", response.text)
    exit()

result = response.json()

# === 5. Display detection probabilities for spaghetti and congee ===
spaghetti_probs = []
congee_probs = []

for prediction in result["predictions"]:
    if prediction["probability"] > 0.3:  # Ngưỡng 30%
        tag_name = prediction["tagName"].lower()
        if tag_name == "spaghetti":
            spaghetti_probs.append(prediction["probability"] * 100)
        elif tag_name == "congee":
            congee_probs.append(prediction["probability"] * 100)

# In kết quả
if spaghetti_probs:
    print(f"Spaghetti: {', '.join(f'{p:.1f}%' for p in spaghetti_probs)}")
else:
    print("Spaghetti: 0.0%")

if congee_probs:
    print(f"Congee: {', '.join(f'{p:.1f}%' for p in congee_probs)}")
else:
    print("Congee: 0.0%")