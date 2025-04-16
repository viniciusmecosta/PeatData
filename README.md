# Peat Data API Documentation

![API Version](https://img.shields.io/badge/API%20Version-1.0.0-blue)
![Authentication](https://img.shields.io/badge/Authentication-Bearer%20Token-green)

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [ESP Endpoints](#esp-endpoints)
  - [App Endpoints](#app-endpoints)
  - [Notification Endpoints](#notification-endpoints)
  - [Admin Endpoints](#admin-endpoints)
- [Request/Response Examples](#requestresponse-examples)
- [Usage Examples](#usage-examples)

## Overview

The Peat Data API provides a comprehensive interface for:

- IoT devices to submit sensor readings
- Mobile applications to retrieve historical data
- Managing notification contacts
- Administrative data management

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/viniciusmecosta/PeatData.git
cd PeatData
```
### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### 3. Create a `.env` file

Create a `.env` file in the root directory of the project with the required environment variables. Example:

```
API_KEY=your_api_key_here
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

## Authentication

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

All endpoints require Bearer Token authentication.

## Endpoints

...

## Usage Examples

### Python Example

```python
import requests

url = "https://api.example.com/esp/temperature-humidity"
headers = {"Authorization": "Bearer YOUR_TOKEN"}
data = {"temperature": 23.5, "humidity": 60.0}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### cURL Example

```bash
curl -X POST \
  https://api.example.com/esp/temperature-humidity \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"temperature":23.5,"humidity":60.0}'
```
