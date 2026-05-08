import streamlit as st
import requests

st.title("Crop Predictor")

n = st.number_input("Nitrogen")
p = st.number_input("Phosphorus")
k = st.number_input("Potassium")

temp = st.number_input("Temperature")
humidity = st.number_input("Humidity")
ph = st.number_input("pH")
rainfall = st.number_input("Rainfall")

if st.button("Predict"):

    data = {
        "n": n,
        "p": p,
        "k": k,
        "temp": temp,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=data
    )

    st.write(response.status_code)
    st.write(response.text)