Healthcare Data API

A lightweight Python REST API prototype for healthcare patient data processing.

The project demonstrates a basic healthcare data workflow:

Patient Data → Validation → De-identification → Storage → API Retrieval → Analytics

Features

- Patient data validation
- Required-field validation
- Automatic patient IDs
- Basic de-identification of patient names
- In-memory patient storage
- Retrieve all patients
- Retrieve an individual patient by ID
- Patient summary analytics
- JSON API responses
- Error handling for invalid requests
- Browser-based testing interface

API Endpoints

Method| Endpoint| Purpose
GET| "/"| Check API status
GET| "/test"| Browser testing interface
POST| "/patients"| Add and validate a patient
GET| "/patients"| Retrieve all patients
GET| "/patients/P001"| Retrieve one patient
GET| "/summary"| Generate patient statistics

Example Patient

Input:

{
    "name": "Ahmed Ali",
    "age": "31",
    "gender": "Male",
    "diagnosis": "Diabetes",
    "medication": "Metformin"
}

Output:

{
    "status": "validated",
    "patient_id": "P001",
    "name": "[DE-IDENTIFIED]",
    "age": "31",
    "gender": "Male",
    "diagnosis": "Diabetes",
    "medication": "Metformin"
}

Example Summary

{
    "status": "success",
    "total_patients": 2,
    "gender_distribution": {
        "Male": 2
    },
    "diagnoses": {
        "Diabetes": 2
    },
    "medications": {
        "Metformin": 2
    }
}

Technology

- Python
- HTTP Server
- JSON
- REST API concepts
- Healthcare data validation
- Basic de-identification

The implementation uses Python's standard library and does not require external packages.

Project Purpose

This is a portfolio prototype exploring healthcare data infrastructure and the processing of patient information through an API layer.

It is designed as a learning and demonstration project and is not intended for production clinical use.

Current Limitations

- Data is stored only in memory.
- Restarting the server clears stored patients.
- No authentication or authorization.
- No database.
- De-identification is intentionally basic.
- No production-grade security, audit logging, or compliance controls.

Future Development

Potential improvements include:

- Database persistence
- Authentication and authorization
- More robust de-identification
- Healthcare interoperability standards such as FHIR
- Audit logging
- Advanced validation
- Hospital system integration
- Secure deployment

Author

HagerElsay
