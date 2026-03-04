import os
import numpy as np
import pandas as pd
import joblib
from django.shortcuts import render
from django.conf import settings
from .models import Prediction

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "housepriceprediction",
    "model",
    "xgboost_house_price_model.pkl"
)
print("MODEL_PATH:", MODEL_PATH)
print("File exists?", os.path.exists(MODEL_PATH))
print("File size (bytes):", os.path.getsize(MODEL_PATH))
model = joblib.load(MODEL_PATH)

# THEN PRINT TYPE
print("Loaded Model Type:", type(model))

DATA_PATH = os.path.join(
    settings.BASE_DIR,
    "data",
    "housing.csv"
)

model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)


def home(request):
    return render(request, 'index.html', {'page': 'descriptive'})


def descriptive(request):
    summary = df.describe().to_html()

    return render(request, 'index.html', {
        'page': 'descriptive',
        'rows': df.shape[0],
        'cols': df.shape[1],
        'summary': summary
    })


def inferential(request):

    corr = df.corr(numeric_only=True)['median_house_value'].to_frame().to_html()

    return render(request, 'index.html', {
        'page': 'inferential',
        'correlation': corr
    })


def prediction(request):
    return render(request, 'index.html', {'page': 'prediction'})


def predict(request):
    if request.method == "POST":

        def get_value(field):
            value = request.POST.get(field)
            if value == "" or value is None:
                return df[field].mean()
            return float(value)

        longitude = get_value("longitude")
        latitude = get_value("latitude")
        housing_median_age = get_value("housing_median_age")
        total_rooms = get_value("total_rooms")
        population = get_value("population")
        households = get_value("households")
        median_income = get_value("median_income")

        input_data = [[
            longitude,
            latitude,
            housing_median_age,
            total_rooms,
            population,
            households,
            median_income,
            0, 1, 0, 0   # default: INLAND
        ]]

        prediction = model.predict(input_data)[0]
        

        Prediction.objects.create(
            longitude=longitude,
            latitude=latitude,
            housing_median_age=housing_median_age,
            total_rooms=total_rooms,
            population=population,
            households=households,
            median_income=median_income,
            predicted_price=prediction
        )

        


        return render(request, "index.html", {
            "page": "result",
            "prediction": round(prediction, 2)
        })
