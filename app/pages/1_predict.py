import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

st.set_page_config(page_title="Price Predictor | AMAC Rental Predictor", layout="wide")

@st.cache_resource
def load_model_assets():

    model_path = BASE_DIR /  "abuja_rent_model.pkl"
    cols_path = BASE_DIR /"feature_columns.pkl"
    try:
        model = joblib.load(model_path)
        feature_cols = joblib.load(cols_path)
        return model, feature_cols
    except Exception as e:
        st.error(f"Error loading model assets. Please ensure .pkl files are in the directory. Details: {e}")
        return None, None

model, feature_cols = load_model_assets()

def determine_tier(district):
    tier_1 = ['Maitama', 'Asokoro', 'Wuse 2', 'Wuse', 'Guzape']
    tier_2 = ['Gwarinpa', 'Jabi', 'Life Camp', 'Katampe', 'Jahi', 'Mabushi', 'Utako', 'Gaduwa', 'Apo', 'Kaura']
    
    if district in tier_1:
        return 'Tier 1 - Luxury'
    elif district in tier_2:
        return 'Tier 2 - Mid-Market'
    else:
        return 'Tier 3 - Affordable'

def get_market_segment(predicted_price):
    if predicted_price >= 15000000:
        return "Ultra-Luxury"
    elif predicted_price >= 8000000:
        return "Premium"
    elif predicted_price >= 3000000:
        return "Mid-Range"
    else:
        return "Budget"

st.title("Rental Price Predictor")
st.markdown("Enter property details below to generate a machine learning estimation of the annual rent.")
st.markdown("---")

if model and feature_cols:
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Property Specifications")
        
        districts = ['Apo', 'Asokoro', 'Central Business District', 'Durumi', 'Gaduwa', 'Galadimawa', 
                     'Garki', 'Guzape', 'Gwarinpa', 'Idu', 'Jabi', 'Jahi', 'Kabo', 'Kado', 'Karmo', 
                     'Karsana', 'Karu', 'Katama', 'Katampe', 'Kaura', 'Kubwa', 'Kukwaba', 'Life Camp', 
                     'Lokogoma', 'Lugbe', 'Mabushi', 'Maitama', 'Utako', 'Wuse', 'Wuse 2', 'Wuye']
        
        property_categories = ['Apartment', 'Duplex', 'Bungalow', 'Self Contain', 'Mini Flat']
        
        selected_district = st.selectbox("Select District", sorted(districts))
        
        selected_category = st.selectbox("Property Category", property_categories)
        
        if selected_category in ["Self Contain", "Mini Flat"]:
            selected_bedrooms = 1
            #st.info("")
        else:
            selected_bedrooms = st.slider("Number of Bedrooms", min_value=1, max_value=6, value=2)
        
        predict_button = st.button("Predict Rent", use_container_width=True)
        
    with col2:
        if predict_button:
            with st.spinner("Analyzing market data..."):
                input_df = pd.DataFrame(columns=feature_cols)
                input_df.loc[0] = 0 
                
                if 'Bedrooms' in feature_cols:
                    input_df.at[0, 'Bedrooms'] = selected_bedrooms
                
                district_col = f"District_{selected_district}"
                if district_col in feature_cols:
                    input_df.at[0, district_col] = 1
                    
                tier = determine_tier(selected_district)
                tier_col = f"District_Tier_{tier}"
                if tier_col in feature_cols:
                    input_df.at[0, tier_col] = 1
                    
                cat_col = f"Property Category_{selected_category}"
                if cat_col in feature_cols:
                    input_df.at[0, cat_col] = 1
                
                input_df = input_df.astype(float)
                log_prediction = model.predict(input_df)[0]
                actual_prediction = np.expm1(log_prediction)
                
                st.subheader("Prediction Results")
                
                metric_col1, metric_col2 = st.columns(2)
                
                with metric_col1:
                    st.metric(
                        label="Estimated Annual Rent",
                        value=f"₦{actual_prediction:,.0f}"
                    )
                
                with metric_col2:
                    segment = get_market_segment(actual_prediction)
                    st.metric(
                        label="Market Segment",
                        value=segment
                    )
                
                st.info(f"Based the Random Forest model, a {selected_bedrooms}-bedroom {selected_category} in {selected_district} is currently valued at approximately **₦{actual_prediction:,.0f}** per annum. This aligns with the {segment} tier of the Abuja real estate market.")
else:
    st.warning("Please ensure the model files are present to use the predictor.")