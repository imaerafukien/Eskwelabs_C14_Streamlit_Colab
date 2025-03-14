import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set page title
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Overall", "Introduction", "Methodology", "Results", "Recommendations"])

# Ensure directories exist
data_dir = "data"
image_dir = "images"
plot_dir = "plots"

os.makedirs(data_dir, exist_ok=True)
os.makedirs(image_dir, exist_ok=True)
os.makedirs(plot_dir, exist_ok=True)

# open cc_clean
cc_clean_path = os.path.join(data_dir, "cc_clean.csv")
if os.path.exists(cc_clean_path):
    df = pd.read_csv(cc_clean_path)
    #st.dataframe(df)
else:
    st.warning("No data file found. Please add a CSV file to `data/` directory.")

# open cc_rfm
cc_rfm_path = os.path.join(data_dir, "cc_rfm.csv")
if os.path.exists(cc_rfm_path):
    rfm_df = pd.read_csv(cc_rfm_path)
    #st.dataframe(rfm_df)
else:
    st.warning("No data file found. Please add a CSV file to `data/` directory.")

# Overall Section
if menu == "Overall":
    st.title("Overall Summary")
    st.markdown('**Adobo Bank wants to expand their current CC offerings by understanding their customer segments.**')
    st.info("“What strategies can we adopt to boost card activation, transaction frequency, and spending volume among our existing customers?”")
    st.info("“How can we strategically target underserved markets or demographics to acquire new customers and grow our market share?”")


# Introduction Section
elif menu == "Introduction":
    st.title("Introduction")
    st.write("Project background and objectives.")

    
    
# Methodology Section
elif menu == "Methodology":
    st.title("Methodology")
    st.write("Describe the approach, techniques, and tools used.")

    st.markdown("""
    - **Step 1**: Data Collection
    - **Step 2**: Data Cleaning
    - **Step 3**: Model Training
    - **Step 4**: Evaluation
    """)

# Results Section
elif menu == "Results":
    st.title("Results")
    st.write("Findings and visualizations.")

    # Load sample data
    data_path = os.path.join(data_dir, "sample_data.csv")
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        st.table(df)
    else:
        st.warning("No data file found. Please add a CSV file to `data/` directory.")

# Recommendations Section
elif menu == "Recommendations":
    st.title("Recommendations")
    st.write("Provide insights and future recommendations.")

    user_recommendation = st.text_area("Write your recommendation...")
    if st.button("Submit Recommendation"):
        st.success("Recommendation submitted!")

# Footer
st.sidebar.write("Developed using Streamlit")
