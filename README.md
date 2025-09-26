# Peat Data API Documentation

<p align="center"> <strong>A comprehensive API for managing data from IoT devices, applications, and notifications.</strong>
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3.9-blue?logo=python&logoColor=white" alt="Python Version"/>
<img src="https://img.shields.io/badge/FastAPI-0.115.12-blue?logo=fastapi&logoColor=white" alt="FastAPI Version"/>
<img src="https://img.shields.io/badge/SQLAlchemy-2.0-blue?logo=sqlalchemy&logoColor=white" alt="SQLAlchemy Version"/>
<img src="https://img.shields.io/badge/Pydantic-2.10-blue" alt="Pydantic Version"/>
<img src="https://img.shields.io/badge/Docker-Supported-blue?logo=docker&logoColor=white" alt="Docker Support"/>
<img src="https://img.shields.io/badge/MQTT-paho--mqtt-green?logo=mqtt" alt="MQTT Client"/>
<img src="https://img.shields.io/badge/license-MIT-green" alt="License"/>
</p>

-----

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [MQTT Client](#mqtt-client)
- [Technologies Utilized](#technologies-utilized)
- [Endpoints](#endpoints)
    - [Temp-Humi Endpoints](#temp-humi-endpoints)
    - [Level Endpoints](#level-endpoints)
    - [Phone Endpoints](#phone-endpoints)
    - [Email Endpoints](#email-endpoints)
    - [Admin Endpoints](#admin-endpoints)
- [Usage Examples](#usage-examples)

-----

## Overview

The **Peat Data API** provides a comprehensive interface for:

- Receiving data from IoT devices via an MQTT server and storing it in the database.
- Allowing mobile applications to retrieve historical data.
- Managing contacts for notifications.
- Administrative functions for data management.

-----

## Getting Started

### 1\. Clone the repository

```bash
git clone https://github.com/viniciusmecosta/PeatData.git
cd PeatData
````

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### 3. Create a `.env` file

Create a `.env` file in the root directory of the project with the required environment variables. Use `example.env` as
a template.

```env
API_TOKEN=your_token_here
MQTT_BROKER=your_broker_here
MQTT_PORT=your_port_here
MQTT_USER=your_user_here
MQTT_PASSWORD=your_password_here
MQTT_TOPIC_SENSOR=your_sensor_topic_here
MQTT_TOPIC_LEVEL=your_level_topic_here
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

---

## Authentication

All API endpoints require Bearer Token authentication. Include the token in the `Authorization` header of each request.

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## MQTT Client

The API acts as an MQTT client, subscribing to topics defined in the environment variables (`MQTT_TOPIC_SENSOR`,
`MQTT_TOPIC_LEVEL`). It processes incoming messages and stores the data in the database using the `paho-mqtt` library.

---

## Technologies Utilized

* **Language:** Python 3.9
* **Framework:** FastAPI
* **ASGI Server:** Uvicorn
* **ORM:** SQLAlchemy
* **Data Validation:** Pydantic
* **MQTT Client:** Paho-MQTT
* **Database:** SQLite
* **Containerization:** Docker
* **Environment Variables:** python-dotenv

---

## Endpoints

### Temp-Humi Endpoints

* `POST /temp-humi`: Submit temperature and humidity data to the database.
* `GET /temp-humi`: Retrieve temperature and humidity data based on query parameters (`avg`, `last`, `days`, `date`).

### Level Endpoints

* `POST /level`: Submit feeder occupation level data to the database.
* `GET /level`: Retrieve level data based on query parameters (`avg`, `last`, `days`, `date`).

### Phone Endpoints

* `POST /phone`: Add a new phone number to the database.
* `GET /phone`: Retrieve all registered phone numbers.

### Email Endpoints

* `POST /email`: Add a new email address to the database.
* `GET /email`: Retrieve all registered email addresses.

### Admin Endpoints

* `POST /generate-temp-humi-data`: Generate mock temperature and humidity data.
* `DELETE /temp-humi`: Delete all sensor data records.
* `POST /generate-level-data`: Generate mock level/distance data.
* `DELETE /level`: Delete all level data records.
* `POST /generate-email/{n}`: Generate `n` mock email records.
* `DELETE /email`: Delete all email records.
* `POST /generate-phone/{n}`: Generate `n` mock phone records.
* `DELETE /phone`: Delete all phone records.

---

## Usage Examples

### Python Example

```python
import requests

url = "http://127.0.0.1:8000/temp-humi"
headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}
data = {"temperature": 23.5, "humidity": 60.0}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### cURL Example

```bash
curl -X POST \
  http://127.0.0.1:8000/temp-humi \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"temperature":23.5,"humidity":60.0}'
```
