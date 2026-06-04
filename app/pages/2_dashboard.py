import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
st.set_page_config(page_title="Market Dashboard | AMAC Rental Dashboard", layout="wide")

@st.cache_data
def load_data():
    data_path = BASE_DIR / "abuja_rental_master_v2.csv"
    try:
        df = pd.read_csv(data_path)
        
        df = df[df['Bedrooms'] <= 6]
        df = df[df['Price (Per Annum)'] <= 150_000_000]
        district_counts = df['District'].value_counts()
        districts_to_keep = district_counts[district_counts >= 10].index
        df = df[df['District'].isin(districts_to_keep)]
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please ensure abuja_rental_master_v2.csv is in the directory.")
        return None

df = load_data()

st.title("Abuja Rental Market Dashboard")
st.markdown("Macro-economic overview of the AMAC rental market based on verified listings.")

if df is not None:
    st.sidebar.header("Filter Dashboard")
    
    all_districts = ['All'] + sorted(df['District'].unique().tolist())
    selected_district_filter = st.sidebar.selectbox("Filter by District", all_districts)
    
    all_categories = ['All'] + sorted(df['Property Category'].unique().tolist())
    selected_category_filter = st.sidebar.selectbox("Filter by Property Category", all_categories)
    
    filtered_df = df.copy()
    if selected_district_filter != 'All':
        filtered_df = filtered_df[filtered_df['District'] == selected_district_filter]
    if selected_category_filter != 'All':
        filtered_df = filtered_df[filtered_df['Property Category'] == selected_category_filter]

    st.sidebar.markdown("---")
    st.sidebar.info("Adjust the filters above to recalculate the metrics and charts dynamically.")

    st.subheader("Dataset Overview")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric("Total Listings", f"{len(filtered_df):,}")
    with m2:
        st.metric("Active Districts", f"{filtered_df['District'].nunique()}")
    with m3:
        avg_rent = filtered_df['Price (Per Annum)'].mean()
        st.metric("Average Rent", f"₦{avg_rent:,.0f}")
    with m4:
        med_rent = filtered_df['Price (Per Annum)'].median()
        st.metric("Median Rent", f"₦{med_rent:,.0f}")
        
    st.markdown("---")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Price Distribution")
        fig_hist = px.histogram(
            filtered_df, 
            x="Price (Per Annum)", 
            nbins=40,
            color_discrete_sequence=['#1f77b4'],
            labels={"Price (Per Annum)": "Annual Rent (Naira)"}
        )
        fig_hist.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_hist, use_container_width=True)
        st.caption("Shows the frequency of different price points. A right-skewed tail indicates the presence of luxury properties.")

    with col2:
        st.subheader("Bedrooms vs Price")
        fig_scatter = px.box(
            filtered_df, 
            x="Bedrooms", 
            y="Price (Per Annum)",
            color_discrete_sequence=['#2ca02c'],
            labels={"Price (Per Annum)": "Annual Rent (Naira)"}
        )
        fig_scatter.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.caption("Illustrates the variance in price based on the number of bedrooms.")

    st.markdown("---")

    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Valuation by Property Category")
        fig_cat_box = px.box(
            filtered_df,
            x="Property Category",
            y="Price (Per Annum)",
            color="Property Category",
            labels={"Price (Per Annum)": "Annual Rent (Naira)"}
        )
        fig_cat_box.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_cat_box, use_container_width=True)
        st.caption("Highlights the base premium attached to specific structural types, such as Duplexes over Apartments.")

    with col4:
        st.subheader("Market Inventory Composition")
        fig_tree = px.treemap(
            filtered_df, 
            path=[px.Constant("Abuja Market"), 'Property Category', 'District'],
            color='Price (Per Annum)',
            color_continuous_scale='Blues',
            labels={"Price (Per Annum)": "Avg Rent"}
        )
        fig_tree.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_tree, use_container_width=True)
        st.caption("Hierarchical view of inventory. Box size represents listing count; darker colors represent higher average prices.")

    st.markdown("---")

    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Listing Volume by Source")
        if 'Source' in filtered_df.columns:
            source_counts = filtered_df['Source'].value_counts().reset_index()
            source_counts.columns = ['Source', 'Listing Volume']
            
            fig_source = px.pie(
                source_counts, 
                names='Source', 
                values='Listing Volume',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_source.update_layout(margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_source, use_container_width=True)
            st.caption("Distribution of property listings across different data sources/platforms.")
        else:
            st.info("The column 'Source' was not found in the dataset.")

    with col6:
        st.subheader("Price/Market Tier Distribution")
        
        def categorize_tier(price):
            if price <= 3_000_000:
                return "Budget (≤₦3m)"
            elif price <= 10_000_000:
                return "Mid-Tier (₦3m - ₦10m)"
            elif price <= 30_000_000:
                return "High-End (₦10m - ₦30m)"
            else:
                return "Luxury (>₦30m)"
                
        filtered_df['Market Tier'] = filtered_df['Price (Per Annum)'].apply(categorize_tier)
        tier_counts = filtered_df['Market Tier'].value_counts().reset_index()
        tier_counts.columns = ['Market Tier', 'Listing Count']
        
        tier_order = ["Budget (≤₦3m)", "Mid-Tier (₦3m - ₦10m)", "High-End (₦10m - ₦30m)", "Luxury (>₦30m)"]
        
        fig_tier = px.bar(
            tier_counts, 
            x='Market Tier', 
            y='Listing Count',
            color='Market Tier',
            category_orders={"Market Tier": tier_order},
            text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_tier.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_tier, use_container_width=True)
        st.caption("Categorization of market inventory into distinct pricing tiers based on annual rent.")

    st.markdown("---")

    if selected_district_filter == 'All':
        st.subheader("Geographical Pricing Hierarchy (Top 15 Districts)")
        
        district_pricing = filtered_df.groupby('District')['Price (Per Annum)'].median().reset_index()
        district_pricing = district_pricing.sort_values(by='Price (Per Annum)', ascending=False).head(15)
        
        fig_bar = px.bar(
            district_pricing, 
            x='District', 
            y='Price (Per Annum)',
            text_auto='.2s',
            color='Price (Per Annum)',
            color_continuous_scale='Blues',
            labels={"Price (Per Annum)": "Median Annual Rent"}
        )
        fig_bar.update_layout(xaxis_tickangle=-45, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.subheader(f"Listing Density in {selected_district_filter}")
        
        fig_detailed_scatter = px.scatter(
            filtered_df,
            x="Bedrooms",
            y="Price (Per Annum)",
            color="Property Category",
            size_max=10,
            opacity=0.7,
            labels={"Price (Per Annum)": "Annual Rent (Naira)"}
        )
        fig_detailed_scatter.update_traces(marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey')))
        fig_detailed_scatter.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_detailed_scatter, use_container_width=True)
        st.caption("Displays individual listings. Use the legend to isolate specific property categories.")