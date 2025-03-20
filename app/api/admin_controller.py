from fastapi import APIRouter

from app.core.constants import DOCUMENT_SENSOR_DISTANCE, DOCUMENT_SENSOR_DATA, DOCUMENT_EMAIL, DOCUMENT_PHONE
from app.service.admin_service import AdminService

router = APIRouter()
admin_service = AdminService()

@router.post("/generate_sensor_data", tags=["ADMIN"])
async def generate_sensor_data_route():
    """
    This route generates mock temperature and humidity data for the past 31 days.
    It generates two records for each day, for a total of 62 records, and stores them in Firebase Firestore.
    Temperature is a random number between 20 and 38, and humidity is a random number between 30 and 85.
    """
    try:
        admin_service.generate_sensor_data()
        return {"message": "Sensor data generated successfully!"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

@router.delete("/sensor-data", tags=["ADMIN"])
async def delete_sensor_data():
    """
    Endpoint to delete all documents from the `sensor_data` collection in Firebase.

    **Response:**
    - Success message when deletion is completed.

    **Example request:**
    ```json
    DELETE /sensor-data
    ```

    **Example response:**
    ```json
    {
      "message": "All sensor data deleted successfully"
    }
    ```
    """
    admin_service.delete_all(DOCUMENT_SENSOR_DATA)
    return {"message": "All sensor data deleted successfully"}

@router.post("/generate_distance_data", tags=["ADMIN"])
async def generate_distance_data_route():
    """
    This route generates mock distance data for the past 31 days.
    It generates two records for each day, for a total of 62 records, and stores them in Firebase Firestore.
    Distance is a random number between 0 and 100 (representing a percentage of the tank filled).
    """
    try:
        admin_service.generate_distance_data()
        return {"message": "Distance data generated successfully!"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

@router.delete("/sensor-distance", tags=["ADMIN"])
async def delete_sensor_distance():
    """
    Endpoint to delete all documents from the `sensor_data` collection in Firebase.

    **Response:**
    - Success message when deletion is completed.

    **Example request:**
    ```json
    DELETE /sensor-distance
    ```

    **Example response:**
    ```json
    {
      "message": "All sensor distance deleted successfully"
    }
    ```
    """
    admin_service.delete_all(DOCUMENT_SENSOR_DISTANCE)
    return {"message": "All sensor distance deleted successfully"}

@router.post("/generate_email_data/{n}", tags=["ADMIN"])
async def generate_email_data_route(n : int):
    """
    This route generates mock distance data for the past 31 days.
    It generates two records for each day, for a total of 62 records, and stores them in Firebase Firestore.
    Distance is a random number between 0 and 100 (representing a percentage of the tank filled).
    """
    try:
        admin_service.generate_email_data(n)
        return {"message": "Distance data generated successfully!"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

@router.delete("/email", tags=["ADMIN"])
async def delete_email():
    """
    Endpoint to delete all documents from the `email` collection in Firebase.

    **Response:**
    - Success message when deletion is completed.

    **Example request:**
    ```json
    DELETE /sensor-distance
    ```

    **Example response:**
    ```json
    {
      "message": "All emails distance deleted successfully"
    }
    ```
    """
    admin_service.delete_all(DOCUMENT_EMAIL)
    return {"message": "All emails deleted successfully"}

@router.post("/generate_phone_data/{n}", tags=["ADMIN"])
async def generate_phone_data_route(n : int):
    """
    This route generates mock distance data for the past 31 days.
    It generates two records for each day, for a total of 62 records, and stores them in Firebase Firestore.
    Distance is a random number between 0 and 100 (representing a percentage of the tank filled).
    """
    try:
        admin_service.generate_phone_data(n)
        return {"message": "Distance data generated successfully!"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

@router.delete("/phone", tags=["ADMIN"])
async def delete_sensor_distance():
    """
    Endpoint to delete all documents from the `phone` collection in Firebase.

    **Response:**
    - Success message when deletion is completed.

    **Example request:**
    ```json
    DELETE /phone
    ```

    **Example response:**
    ```json
    {
      "message": "All phones deleted successfully"
    }
    ```
    """
    admin_service.delete_all(DOCUMENT_PHONE)
    return {"message": "All phones deleted successfully"}