from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("model.pkl")
le = joblib.load("label_encoder.pkl")

@app.post("/predict")
def predict(data: dict):

    values = np.array([[
        data["n"],
        data["p"],
        data["k"],
        data["temp"],
        data["humidity"],
        data["ph"],
        data["rainfall"]
    ]])

    prediction = model.predict(values)

    crop_name = le.inverse_transform(prediction)

    return {"prediction": crop_name[0]}