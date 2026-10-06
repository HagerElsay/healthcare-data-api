from http.server import BaseHTTPRequestHandler, HTTPServer
import json

patient_counter = 0
patients = []


def validate_patient(patient):
    required_fields = [
        "name",
        "age",
        "gender",
        "diagnosis",
        "medication"
    ]

    missing_fields = []

    for field in required_fields:
        if field not in patient or patient[field] == "":
            missing_fields.append(field)

    if missing_fields:
        return False, missing_fields

    return True, []


def process_patient(patient):
    global patient_counter

    valid, missing_fields = validate_patient(patient)

    if not valid:
        return {
            "status": "error",
            "message": "Missing required fields",
            "missing_fields": missing_fields
        }

    patient_counter += 1
    patient_id = f"P{patient_counter:03d}"

    processed_patient = {
        "status": "validated",
        "patient_id": patient_id,
        "name": "[DE-IDENTIFIED]",
        "age": patient["age"],
        "gender": patient["gender"],
        "diagnosis": patient["diagnosis"],
        "medication": patient["medication"]
    }

    patients.append(processed_patient)

    return processed_patient


def create_summary():
    gender_count = {}
    diagnosis_count = {}
    medication_count = {}

    for patient in patients:
        gender = patient["gender"]
        diagnosis = patient["diagnosis"]
        medication = patient["medication"]

        gender_count[gender] = gender_count.get(gender, 0) + 1
        diagnosis_count[diagnosis] = diagnosis_count.get(diagnosis, 0) + 1
        medication_count[medication] = medication_count.get(medication, 0) + 1

    return {
        "status": "success",
        "total_patients": len(patients),
        "gender_distribution": gender_count,
        "diagnoses": diagnosis_count,
        "medications": medication_count
    }


class HealthcareAPI(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":

            self.send_json(
                200,
                {
                    "message": "Healthcare Data API",
                    "status": "running"
                }
            )

        elif self.path == "/patients":

            self.send_json(
                200,
                {
                    "status": "success",
                    "count": len(patients),
                    "patients": patients
                }
            )

        elif self.path.startswith("/patients/"):

            patient_id = self.path.split("/")[-1]

            for patient in patients:

                if patient["patient_id"] == patient_id:
                    self.send_json(200, patient)
                    return

            self.send_json(
                404,
                {
                    "status": "error",
                    "message": "Patient not found",
                    "patient_id": patient_id
                }
            )

        elif self.path == "/summary":

            self.send_json(200, create_summary())

        elif self.path == "/test":

            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Healthcare Data API Test</title>
            </head>

            <body>

            <h2>Healthcare Data API</h2>

            <input id="name" placeholder="Name"><br><br>
            <input id="age" placeholder="Age"><br><br>
            <input id="gender" placeholder="Gender"><br><br>
            <input id="diagnosis" placeholder="Diagnosis"><br><br>
            <input id="medication" placeholder="Medication"><br><br>

            <button onclick="sendPatient()">Submit Patient</button>

            <pre id="result"></pre>

            <script>

            function sendPatient() {

                const patient = {
                    name: document.getElementById("name").value,
                    age: document.getElementById("age").value,
                    gender: document.getElementById("gender").value,
                    diagnosis: document.getElementById("diagnosis").value,
                    medication: document.getElementById("medication").value
                };

                fetch("/patients", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(patient)
                })
                .then(response => response.json())
                .then(data => {

                    document.getElementById("result").textContent =
                        JSON.stringify(data, null, 4);

                })
                .catch(error => {

                    document.getElementById("result").textContent =
                        "Error: " + error;

                });
            }

            </script>

            </body>
            </html>
            """

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        else:

            self.send_json(
                404,
                {
                    "status": "error",
                    "message": "Endpoint not found",
                    "path": self.path
                }
            )

    def do_POST(self):

        if self.path != "/patients":

            self.send_json(
                404,
                {
                    "status": "error",
                    "message": "Endpoint not found",
                    "path": self.path
                }
            )

            return

        content_length = int(
            self.headers.get("Content-Length", 0)
        )

        if content_length == 0:

            self.send_json(
                400,
                {
                    "status": "error",
                    "message": "Request body is empty"
                }
            )

            return

        body = self.rfile.read(content_length)

        try:

            patient = json.loads(body)

        except json.JSONDecodeError:

            self.send_json(
                400,
                {
                    "status": "error",
                    "message": "Invalid JSON"
                }
            )

            return

        if not isinstance(patient, dict):

            self.send_json(
                400,
                {
                    "status": "error",
                    "message": "Patient data must be a JSON object"
                }
            )

            return

        result = process_patient(patient)

        if result["status"] == "error":
            self.send_json(400, result)
        else:
            self.send_json(201, result)

    def send_json(self, status_code, data):

        self.send_response(status_code)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.end_headers()

        self.wfile.write(
            json.dumps(
                data,
                indent=4
            ).encode()
        )


server = HTTPServer(
    ("0.0.0.0", 8000),
    HealthcareAPI
)

print("Healthcare Data API running on port 8000...")
print("GET  /")
print("GET  /patients")
print("GET  /patients/P001")
print("GET  /summary")
print("GET  /test")
print("POST /patients")

server.serve_forever()
