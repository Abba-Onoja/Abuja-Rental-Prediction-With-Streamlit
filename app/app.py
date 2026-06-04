import streamlit as st
from pathlib import Path

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
    """)

    st.markdown("---")
    
    # --- DATA DOWNLOAD SECTION ---
    st.subheader("Datasets")
    st.markdown("Download the datasets used in this project for independent research or auditing purposes.")
    
    d_col1, d_col2 = st.columns(2)
    
    master_data_path = Path("abuja_rental_master_v2.csv")
    processed_data_path = Path("processed_abuja_rentals.csv")

    with d_col1:
        st.markdown("**Master Dataset**")
        st.info("Contains the full set of scraped listings after initial cleaning and deduplication.")
        
        if master_data_path.exists():
            st.download_button(
                label="Download Master CSV",
                data=master_data_path.read_bytes(),
                file_name=master_data_path.name,
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.error("Master dataset file not found.")

    with d_col2:
        st.markdown("**Processed Dataset**")
        st.info("The final feature-engineered dataset used for training the Random Forest model.")
        
        if processed_data_path.exists():
            st.download_button(
                label="Download Processed CSV",
                data=processed_data_path.read_bytes(),
                file_name=processed_data_path.name,
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.error("Processed dataset file not found.")

    with st.sidebar:
        st.markdown("[My Portfolio](https://github.com/Abba-Onoja)") 

    st.markdown("---")
    st.caption("Built by Abba Onoja")

if __name__ == "__main__":
    main()