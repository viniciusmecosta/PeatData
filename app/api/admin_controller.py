from fastapi import APIRouter

from app.service.admin_service import AdminService

router = APIRouter()
admin_service = AdminService()


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
    admin_service.delete_all_sensor_data()
    return {"message": "All sensor data deleted successfully"}


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
    admin_service.delete_all_sensor_distance()
    return {"message": "All sensor distance deleted successfully"}


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
