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
    st.subheader('Adobo Bank is a bank diving into data driven decision making. We as their data scientist team will provide insights and recommendations based on Adobo Bank\'s data')
    # open logo.png from image_dir
    logo_path = os.path.join(image_dir, "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width = 600)
    else:
        st.warning("No image file found. Please add an image to `images/` directory.")
    st.write("We aim to know who are Adobo Bank's customers, what the bank's current data quality is, how to improve data gathering and from their current set of data, how can we contribute to Adobo Bank's growth?")


# Introduction Section
elif menu == "Introduction":
    st.title("Introduction")
    st.write("Project background and objectives.")

    
    
# Methodology Section
elif menu == "Methodology":
    st.title("Methodology")
    st.write("Describe the approach, techniques, and tools used.")

    st.markdown("""
    - **Step 1**: Preprocessing
    - **Step 2**: Exploratory Data Analysis (EDA)
    - **Step 3**: K Means Clustering
    - **Step 4**: Cluster Analysis
    - **Step 5**: Interpretation and Recommendations
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
