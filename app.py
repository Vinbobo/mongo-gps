#MongoDB
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# MongoDB config via environment variables (set these in Render -> Environment)
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://banhbaobeo2205:lm2hiCLXp6B0D7hq@cluster0.festnla.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.getenv("DB_NAME", "Sun_Database")

# Init Mongo client once
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["HR_GPS_Attendance"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/checkin", methods=["POST"])
def checkin():
    try:
        data = request.get_json(force=True, silent=False)
        emp_id = data.get("EmployeeId")
        emp_name = data.get("EmployeeName")
        latitude = data.get("Latitude")
        longitude = data.get("Longitude")

        if not all([emp_id, emp_name, latitude, longitude]):
            return jsonify({"status": "error", "message": "Thiếu dữ liệu bắt buộc"}), 400

        doc = {
            "EmployeeId": str(emp_id),
            "EmployeeName": str(emp_name),
            "CheckInTime": datetime.now(),
            "Latitude": float(latitude),
            "Longitude": float(longitude),
            "Status": "Checked-in"
        }
        collection.insert_one(doc)
        return jsonify({"status": "success", "message": "Chấm công thành công"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # For local testing; Render will use gunicorn
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
