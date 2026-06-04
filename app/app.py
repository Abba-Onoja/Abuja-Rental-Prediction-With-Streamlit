# app.py
import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="AMAC Rental Intelligence System",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("AMAC Rental Prediction and Dashboard")
    
    st.markdown("---")
    
    st.markdown("""
    ### Welcome to the AMAC Intelligence Portal
    
    This application is designed to bring transparency and predictive power to the Abuja Municipal Area Council (AMAC) real estate market. 
    
    Built on over 4,000 consolidated rental listings, this system provides tools for both prospective tenants and real estate professionals.
    
    **Navigation:**
    Please use the sidebar on the left to navigate between the two primary modules:
    
    * **1. Rental Price Predictor:** Utilize a Random Forest machine learning model to estimate the annual rent of a property based on its characteristics and district tier.
    * **2. Market Dashboard:** Explore macro-level trends, distribution metrics, and geographical pricing hierarchies across the Abuja metropolis.
    
    ---
    *Built by Abba Onoja*
    """)

if __name__ == "__main__":
    main()