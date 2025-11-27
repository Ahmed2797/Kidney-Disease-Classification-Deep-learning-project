import streamlit as st
import requests
from PIL import Image

st.set_page_config(page_title="Kidney Disease Classifier", layout="centered")
st.title("🩺 Kidney Disease Classification")

uploaded_file = st.file_uploader("Upload CT Scan Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Preview image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    if st.button("Predict"):
        try:
            api_url = "http://localhost:8000/predict"

            # Send file to API
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

            response = requests.post(api_url, files=files)

            if response.status_code == 200:
                result = response.json()
                st.success(f"Prediction: {result.get('prediction')}")
                st.write(f"Confidence: {result.get('confidence')}")
            else:
                st.error(f"Server error: {response.text}")

        except Exception as e:
            st.error(f"Error: {e}")


## streamlit run stm.py
