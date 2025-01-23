import streamlit as st

# Define the prediction function
def predict_soil_fertility(features):
    ranges = {
        'pH': {'optimal': (6.0, 6.5)},
        'EC': {'optimal': (0.8, 1.8)},
        'OC': {'optimal': (0.28, 6.00)},
        'N': {'optimal': (0.03, 0.07)},
        'P': {'optimal': (0.10, 0.225)},
        'K': {'optimal': (1.28, 2.77)},
        'Zn': {'optimal': (0.001, 0.005)},
        'Fe': {'optimal': (0.01, 0.05)},
        'Cu': {'optimal': (5, 20)},
        'Mn': {'optimal': (0.002, 0.005)},
        'Cl': {'optimal': (0.1, 0.5)},
        'CaCO3': {'optimal': (20, 48)},
        'OM': {'optimal': (3, 5)},
        'Sand': {'optimal': (40, 60)},
        'Silt': {'optimal': (20, 40)},
        'Clay': {'optimal': (20, 40)},
        'CEC': {'optimal': (10, 20)},
        'Boron': {'optimal': (0.5, 1.0)},
        'Magnesium': {'optimal': (50, 150)},
        'NPK': {'optimal': 'Balanced'},
        'EC2': {'optimal': (0.8, 1.8)},
        'PH2': {'optimal': (36, 42)},
        'S': {'optimal': (0.1, 0.4)}
    }

    recommendations = {
        'pH': "Add lime to increase pH or sulfur to decrease it.",
        'EC': "Ensure proper drainage or leach the soil to reduce salinity.",
        'OC': "Incorporate organic matter like compost or manure.",
        'N': "Add nitrogen-rich fertilizers like urea or ammonium nitrate.",
        'P': "Use phosphate fertilizers such as superphosphate or bone meal.",
        'K': "Apply potash-based fertilizers like potassium sulfate.",
        'Zn': "Use zinc sulfate or foliar sprays of zinc solution.",
        'Fe': "Incorporate iron chelates or iron-rich organic compost.",
        'Cu': "Add copper sulfate or use copper-based foliar sprays.",
        'Mn': "Apply manganese sulfate or use chelated manganese fertilizers.",
        'Cl': "Ensure proper drainage or use gypsum to balance chloride levels.",
        'CaCO3': "Add lime to adjust calcium carbonate levels.",
        'OM': "Increase organic matter by adding compost or green manure.",
        'Sand': "Improve soil structure by mixing in organic matter.",
        'Silt': "Avoid soil compaction and use cover crops to balance silt levels.",
        'Clay': "Add organic matter to improve aeration and drainage.",
        'CEC': "Add organic matter to increase cation exchange capacity.",
        'Boron': "Apply borax or boric acid in small quantities.",
        'Magnesium': "Use magnesium sulfate (Epsom salts) or dolomite lime.",
        'NPK': "Balance NPK by using appropriate fertilizers for the deficient element.",
        'EC2': "Ensure proper irrigation and drainage to maintain EC.",
        'PH2': "Adjust soil pH with lime or sulfur based on the requirement.",
        'S': "Incorporate sulfur fertilizers like gypsum or elemental sulfur."
    }

    organic_matter_suggestions = {
        'pH': "Compost, peat moss, or leaf mulch.",
        'EC': "Well-composted organic matter or green manure.",
        'OC': "Compost, vermicompost, or farmyard manure.",
        'N': "Animal manure, green manure, or composted kitchen waste.",
        'P': "Bone meal, rock phosphate, or poultry manure.",
        'K': "Wood ash, banana peels, or composted manure.",
        'Zn': "Zinc-enriched compost or poultry litter.",
        'Fe': "Iron-rich compost or organic mulch.",
        'Cu': "Copper-enriched compost or bio-fertilizers.",
        'Mn': "Manganese-enriched compost or organic fertilizers.",
        'Cl': "Well-rotted manure or gypsum-based organic matter.",
        'CaCO3': "Crushed eggshells or agricultural lime.",
        'OM': "Composted manure, peat, or cover crops.",
        'Sand': "Organic compost or well-aged manure.",
        'Silt': "Organic mulch or cover crops like legumes.",
        'Clay': "Organic compost or gypsum.",
        'CEC': "High-organic-matter compost or humus-rich soil.",
        'Boron': "Borax-treated compost or bio-fertilizers.",
        'Magnesium': "Dolomite lime or magnesium-enriched compost.",
        'NPK': "Balanced organic fertilizers or compost tea.",
        'EC2': "Composted organic matter or biochar.",
        'PH2': "Organic sulfur amendments or compost.",
        'S': "Sulfur-rich compost or gypsum."
    }

    infertile_features = []
    infertility_reasons = {
        'pH': "Soil pH is either too high (alkaline) or too low (acidic), affecting nutrient availability.",
        'EC': "High electrical conductivity (EC) indicates excessive salinity, which can reduce plant growth.",
        'OC': "Low organic carbon (OC) results in poor soil structure and fertility.",
        'N': "Low nitrogen (N) levels cause poor plant growth and reduced crop yield.",
        'P': "Low phosphorus (P) levels result in poor root development and weak plant growth.",
        'K': "Potassium (K) deficiency leads to poor root growth and reduced disease resistance.",
        'Zn': "Zinc (Zn) deficiency results in poor growth and chlorosis.",
        'Fe': "Iron (Fe) deficiency causes yellowing of leaves and poor plant growth.",
        'Cu': "Copper (Cu) deficiency leads to stunted growth and poor seed production.",
        'Mn': "Manganese (Mn) deficiency causes poor root development and chlorosis.",
        'Cl': "Excess chloride (Cl) reduces plant growth and may cause toxicity.",
        'CaCO3': "Too much calcium carbonate (CaCO3) can raise soil pH and cause nutrient imbalances.",
        'OM': "Lack of organic matter (OM) results in poor soil structure and low water retention.",
        'Sand': "High sand content results in poor water retention and nutrient holding capacity.",
        'Silt': "High silt content can cause compaction and poor drainage.",
        'Clay': "Excessive clay content can cause poor drainage and aeration, leading to root diseases.",
        'CEC': "Low Cation Exchange Capacity (CEC) means the soil can't hold enough nutrients for plants.",
        'Boron': "Boron deficiency affects flowering and fruit development.",
        'Magnesium': "Low magnesium levels reduce chlorophyll production and cause leaf discoloration.",
        'NPK': "Imbalanced NPK ratio leads to poor plant growth and nutrient deficiencies.",
        'EC2': "High EC indicates salinity, which can reduce soil fertility and plant growth.",
        'PH2': "Inappropriate pH levels reduce nutrient availability.",
        'S': "Low sulfur (S) levels affect protein synthesis and reduce crop yield."
    }

    infertile_details = {}

    for feature, value in features.items():
        if feature in ranges:
            range_info = ranges[feature]
            if isinstance(value, str) and feature == "NPK":
                if value != range_info['optimal']:
                    infertile_features.append(feature)
            elif isinstance(value, (float, int)):
                if not (range_info['optimal'][0] <= value <= range_info['optimal'][1]):
                    infertile_features.append(feature)

    if not infertile_features:
        return "Fertile", None

    infertile_details = {
        feature: {
            'issue': infertility_reasons.get(feature, "No issue specified"),
            'recommendation': recommendations.get(feature, "No recommendation available"),
            'organic_matter': organic_matter_suggestions.get(feature, "No organic matter suggestion available")
        }
        for feature in infertile_features
    }
    return "Infertile", infertile_details

# Streamlit app
st.title("Soil Fertility Prediction")

# Input fields for soil properties
features = {
    'pH': float(st.text_input("Enter pH:", "6.5")),
    'EC': float(st.text_input("Enter EC (%):", "1.0")),
    'OC': float(st.text_input("Enter OC (%):", "3.0")),
    'N': float(st.text_input("Enter N (%):", "0.05")),
    'P': float(st.text_input("Enter P (%):", "0.15")),
    'K': float(st.text_input("Enter K (%):", "2.0")),
    'Zn': float(st.text_input("Enter Zn (%):", "0.003")),
    'Fe': float(st.text_input("Enter Fe (%):", "0.03")),
    'Cu': float(st.text_input("Enter Cu (%):", "0.0007")),
    'Mn': float(st.text_input("Enter Mn (%):", "0.003")),
    'Cl': float(st.text_input("Enter Cl (%):", "0.15")),
    'CaCO3': float(st.text_input("Enter CaCO3 (%):", "30")),
    'OM': float(st.text_input("Enter OM (%):", "4.0")),
    'Sand': float(st.text_input("Enter Sand (%):", "50")),
    'Silt': float(st.text_input("Enter Silt (%):", "25")),
    'Clay': float(st.text_input("Enter Clay (%):", "25")),
    'CEC': float(st.text_input("Enter CEC (cmol/kg):", "15")),
    'Boron': float(st.text_input("Enter Boron (ppm):", "0.8")),
    'Magnesium': float(st.text_input("Enter Magnesium (%):", "0.12")),
    'NPK': st.selectbox("NPK Fertilizer (Balanced/Unbalanced):", ["Balanced", "Unbalanced"]),
    'EC2': float(st.text_input("Enter EC2 (%):", "1.0")),
    'PH2': float(st.text_input("Enter PH2:", "40")),
    'S': float(st.text_input("Enter S (%):", "0.25"))
}

# Button to trigger prediction
if st.button("Predict Soil Fertility"):
    fertility_status, infertile_details = predict_soil_fertility(features)

    if fertility_status == "Fertile":
        st.success(f"The soil is predicted to be: **{fertility_status}**")
    else:
        st.error(f"The soil is predicted to be: **{fertility_status}**")
        st.write("Issues with the following parameters:")
        for feature, details in infertile_details.items():
            st.write(f"**{feature}**: {details['issue']}")
            st.write(f"  - Recommendation: {details['recommendation']}")
            st.write(f"  - Organic Matter Suggestion: {details['organic_matter']}")
        
        # Generate report
        report = ""
        for feature, details in infertile_details.items():
            report += f"{feature}:\n{details['issue']}\nRecommendation: {details['recommendation']}\nOrganic Matter Suggestion: {details['organic_matter']}\n\n"
        
        # Download button for the report
        st.download_button("Download the report", report, "soil_report.txt", "text/plain")
