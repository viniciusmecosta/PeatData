# from fastapi import APIRouter
#
# from app.core.constants import (
#     DOCUMENT_SENSOR_DISTANCE,
#     DOCUMENT_SENSOR_DATA,
#     DOCUMENT_EMAIL,
#     DOCUMENT_PHONE,
# )
# from app.service.admin_service import AdminService
#
# router = APIRouter(prefix="/admin")
# admin_service = AdminService()
#
#
# @router.post("/generate-sensor-data", tags=["ADMIN"])
# async def generate_sensor_data():
#     """
#     Generates mock temperature and humidity data for the past 31 days.
#     """
#     try:
#         admin_service.generate_sensor_data()
#         return {"message": "Sensor data generated successfully!"}
#     except Exception as e:
#         return {"error": f"An error occurred: {str(e)}"}
#
#
# @router.delete("/sensor-data", tags=["ADMIN"])
# async def delete_sensor_data():
#     """
#     Deletes all documents from the `sensor_data` collection in Firebase.
#     """
#     admin_service.delete_all(DOCUMENT_SENSOR_DATA)
#     return {"message": "All sensor data deleted successfully"}
#
#
# @router.post("/generate-distance-data", tags=["ADMIN"])
# async def generate_distance_data():
#     """
#     Generates mock distance data for the past 31 days.
#     """
#     try:
#         admin_service.generate_distance_data()
#         return {"message": "Distance data generated successfully!"}
#     except Exception as e:
#         return {"error": f"An error occurred: {str(e)}"}
#
#
# @router.delete("/sensor-distance", tags=["ADMIN"])
# async def delete_sensor_distance():
#     """
#     Deletes all documents from the `sensor_distance` collection in Firebase.
#     """
#     admin_service.delete_all(DOCUMENT_SENSOR_DISTANCE)
#     return {"message": "All sensor distance data deleted successfully"}
#
#
# @router.post("/generate-email/{n}", tags=["ADMIN"])
# async def generate_email_data(n: int):
#     """
#     Generates mock email data with `n` records and stores them in Firebase Firestore.
#     """
#     try:
#         admin_service.generate_email_data(n)
#         return {"message": "Email data generated successfully!"}
#     except Exception as e:
#         return {"error": f"An error occurred: {str(e)}"}
#
#
# @router.delete("/email", tags=["ADMIN"])
# async def delete_email():
#     """
#     Deletes all documents from the `email` collection in Firebase.
#     """
#     admin_service.delete_all(DOCUMENT_EMAIL)
#     return {"message": "All emails deleted successfully"}
#
#
# @router.post("/generate-phone/{n}", tags=["ADMIN"])
# async def generate_phone_data(n: int):
#     """
#     Generates mock phone data with `n` records and stores them in Firebase Firestore.
#     """
#     try:
#         admin_service.generate_phone_data(n)
#         return {"message": "Phone data generated successfully!"}
#     except Exception as e:
#         return {"error": f"An error occurred: {str(e)}"}
#
#
# @router.delete("/phone", tags=["ADMIN"])
# async def delete_phone():
#     """
#     Deletes all documents from the `phone` collection in Firebase.
#     """
#     admin_service.delete_all(DOCUMENT_PHONE)
#     return {"message": "All phones deleted successfully"}
