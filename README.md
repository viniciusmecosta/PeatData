# Peat Data API Documentation

![API Version](https://img.shields.io/badge/API%20Version-1.0.0-blue)
![Authentication](https://img.shields.io/badge/Authentication-Bearer%20Token-green)

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [ESP Endpoints](#esp-endpoints)
  - [App Endpoints](#app-endpoints)
  - [Notification Endpoints](#notification-endpoints)
  - [Admin Endpoints](#admin-endpoints)
- [Request/Response Examples](#requestresponse-examples)
- [Data Schemas](#data-schemas)
- [Error Handling](#error-handling)
- [Usage Examples](#usage-examples)

## Overview

The Peat Data API provides a comprehensive interface for:

- IoT devices to submit sensor readings
- Mobile applications to retrieve historical data
- Managing notification contacts
- Administrative data management

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