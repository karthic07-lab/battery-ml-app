from flask import Flask, request, jsonify, render_template_string
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load model
model = joblib.load("model.joblib")

# 🌐 MODERN UI
@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Battery AI</title>
        <style>
            body {
                font-family: Arial;
                background: linear-gradient(to right, #1e3c72, #2a5298);
                color: white;
                text-align: center;
                padding: 50px;
            }
            .card {
                background: white;
                color: black;
                padding: 30px;
                border-radius: 15px;
                width: 300px;
                margin: auto;
            }
            input {
                padding: 10px;
                margin: 10px;
                width: 90%;
            }
            button {
                padding: 10px;
                background: #2a5298;
                color: white;
                border: none;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <h1>🔋 Battery Health Predictor</h1>
        <div class="card">
            <form action="/predict_form" method="post">
                <input name="voltage" placeholder="Voltage"><br>
                <input name="current_percentage" placeholder="Current %"><br>
                <input name="temperature" placeholder="Temperature"><br>
                <button type="submit">Predict</button>
            </form>
        </div>
    </body>
    </html>
    """)

# 📊 FORM OUTPUT
@app.route('/predict_form', methods=['POST'])
def predict_form():
    data = {
        'voltage': float(request.form['voltage']),
        'current_percentage': float(request.form['current_percentage']),
        'temperature': float(request.form['temperature'])
    }

    df = pd.DataFrame([data])
    pred = model.predict(df)[0]

    return f"<h2>Prediction: {pred}</h2><a href='/'>Back</a>"

# 📡 API (ESP32)
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame([data])
    pred = model.predict(df)[0]
    return jsonify({"prediction": str(pred)})

# 🚀 Render fix
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
