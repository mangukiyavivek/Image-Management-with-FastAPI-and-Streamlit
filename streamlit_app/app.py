import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")

st.title("Image Manager")

# Upload Image
st.header("Upload Image")
upload_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
if upload_file is not None:
    files = {"file": (upload_file.name, upload_file, upload_file.type)}
    response = requests.post(f"{FASTAPI_URL}/upload/", files=files)
    if response.status_code == 200:
        st.success("Image uploaded successfully!")
    else:
        st.error("Failed to upload image.")

# Get Image
st.header("Get Image")
image_id = st.number_input("Enter Image ID to retrieve", min_value=1)
if st.button("Get Image"):
    response = requests.get(f"{FASTAPI_URL}/images/{image_id}")
    if response.status_code == 200:
        image_data = response.json()
        st.image(image_data["url"], caption=image_data["name"], use_column_width=True)
    else:
        st.error("Image not found.")
        

# Delete Image
st.header("Delete Image")
delete_image_id = st.number_input("Enter Image ID to delete", min_value=1, key="delete_image_id")
if st.button("Delete Image"):
    response = requests.delete(f"{FASTAPI_URL}/images/{delete_image_id}")
    if response.status_code == 200:
        st.success("Image deleted successfully!")
    else:
        st.error("Failed to delete image.")
