import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input

# Define optimal nutrient ranges for fertility
optimal_ranges = {
    'pH': (6.0, 6.5),
    'EC': (0.8, 1.8),
    'OC': (0.28, 6.00),
    'N': (0.03, 0.07),
    'P': (0.10, 0.225),
    'K': (1.28, 2.77),
    'Zn': (0.001, 0.005),
    'Fe': (0.01, 0.05),
    'Cu': (5, 20),
    'Mn': (0.002, 0.005),
    'Cl': (0.1, 0.5),
    'CaCO3': (20, 48),
    'OM': (3, 5),
    'Sand': (40, 60),
    'Silt': (20, 40),
    'Clay': (20, 40),
    'CEC': (10, 20),
    'Boron': (0.5, 1.0),
    'Magnesium': (50, 150),
    'S': (0.1, 0.4)
}

# Streamlit App
st.title("Soil Fertility Prediction")

# Input fields for soil properties
features = {}
for nutrient, (min_val, max_val) in optimal_ranges.items():
    features[nutrient] = st.number_input(
        f"Enter {nutrient} value:",
        min_value=float(min_val) * 0.5,
        max_value=float(max_val) * 1.5,
        value=float((min_val + max_val) / 2)
    )

# Define Maintenance Recommendations for Alluvial Soil
maintenance_recommendations = [
    "Practice crop rotation to prevent nutrient depletion.",
    "Use green manure and organic compost to enhance soil fertility.",
    "Ensure proper irrigation to prevent erosion and nutrient leaching.",
    "Regularly test soil nutrients and adjust fertilization accordingly.",
    "Encourage microbial activity with organic matter and biofertilizers."
]

# Initialize variables
fertility_status = None
deficient_nutrients = []

# Predict Soil Fertility
if st.button("Predict Soil Fertility"):
    # Check if any nutrient is outside the optimal range
    deficient_nutrients = []
    for param, value in features.items():
        min_val, max_val = optimal_ranges[param]
        if value < min_val or value > max_val:
            deficient_nutrients.append(param)
    
fertility_status = "Infertile" if deficient_nutrients else "Fertile"
st.write(f"The soil is predicted to be: **{fertility_status}**")

report_content = f"Soil Fertility Analysis Report\n\nSoil Status: {fertility_status}\n\n"

if fertility_status == "Infertile":
    st.error("Soil is Infertile! Below are recommendations to improve fertility:")
    report_content += "Nutrient Deficiencies & Recommendations:\n"
    for param in deficient_nutrients:
        issue = "Too Low" if features[param] < optimal_ranges[param][0] else "Too High"
        report_content += f"- {param}: {features[param]} ({issue}). Adjust accordingly.\n"
else:
    st.success("Soil is Fertile! Follow these best practices to maintain fertility:")
    report_content += "Best Practices for Alluvial Soil Maintenance:\n"
    for tip in maintenance_recommendations:
        st.write(f" {tip}")
        report_content += f"- {tip}\n"

st.download_button("Download Soil Report", report_content, "soil_fertility_report.txt", "text/plain")


if fertility_status != "Infertile":
    st.link_button("Crop Recommendation", "https://5cr5vpjlbaumuzpq7unbic.streamlit.app/")
