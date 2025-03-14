import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import os

# Set page title
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Overall", "Introduction", "Methodology", "Scope & Limitations","Results", "Recommendations"])

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
    st.subheader("Adobo Bank wants to expand their current CC offerings by understanding their customer segments.")
    st.markdown("""
    - **Demographic Profiles and Spending Behavior**: Understand our customers better through exploratory data analysis and RFM analysis.

    - **Customer Segmentation**: Segment customers based on their spending behavior or banking transactions.

    - **Analysis & Initial Recommendation**: Provide initial recommendation for CC expansion based on customer segmentation results

    - **Future Project Recommendation**: Generate proof-of-concept (POC) for future project recommendation to provide better CC offerings for customers.

    """)

    
    
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

# Scope & Limitations
elif menu == "Scope & Limitations":
    st.title("Data Preprocessing and Scope & Limitations")

    st.subheader("Data Transaction Period")
    st.write("Customer transactions covered the period January 01, 2020 to December 07, 2021.")
  
    st.subheader("Current Date")
    st.write("Current date set to January 01, 2022.")

    st.subheader("Transaction Category Types")
    st.write("Original transaction categories were categorized into 7 transaction types (entertainment, transportation, food & essentials, health & wellness, home & family, shopping & miscellaneous, and others).")
    
    st.subheader("Job Types")
    st.write("Original job entries were categorized into 8 job types (Creative, Media & Design; Education & Training; Engineering & Infrastructure; Finance, Business & Management; Healthcare & Wellbeing; Public Service & Administration; Retail, Hospitality & Customer Service; Science, Technology & IT).")
    
    st.subheader("Customer Lifetime Value (CLV)")
    st.write("Average spending x Frequency / Customer Tenure")

# Results Section
elif menu == "Results":
    st.title("Results")
    st.write("Findings and visualizations.")

    df = pd.read_csv('data/cc_clean.csv')
    rfm_df = pd.read_csv('data/cc_rfm.csv')
    # map age profile of acct_num in df by using date of birth(dob) column to their respective generation "Greatest": 1901-1927, "Silent": 1928-1945, "Baby Boomer": 1946-1964, "Gen X": 1965-1981
    df['age'] = 2022 - pd.to_datetime(df['dob'], format='%d/%m/%Y').dt.year
    df['yob'] = pd.to_datetime(df['dob'], format='%d/%m/%Y').dt.year
    yob_df = df.groupby('acct_num').agg({'yob':'max','age':'max'})
    yob_df = yob_df.reset_index()
    rfm_df = rfm_df.merge(yob_df[['acct_num','yob','age']], on='acct_num', how='left')
    rfm_df['generation'] = pd.cut(rfm_df['yob'], bins=[1901, 1927, 1945, 1964, 1981], labels=['Greatest', 'Silent', 'Baby Boomer', 'Gen X'])
    # generate bar graph showing acct_num count by generation
    st.subheader("Demographic Profile of Adobo Bank Customers")
    st.bar_chart(rfm_df['generation'].value_counts())
    st.write(rfm_df['age'].describe())
    st.caption("Out of 88 unique customers, majority of Adobo Bank Customers belong in the Baby Boomer Generation (52 customers). ")
    st.caption("All of Adobo Bank's customers are over 55 years old")
    st.divider()
    # create a horizontal bar graph using plotly of trans_num value_counts per category_group in df, sort highest to lowest



# Recommendations Section
elif menu == "Recommendations":
    st.title("Recommendations")
    st.write("Provide insights and future recommendations.")

    user_recommendation = st.text_area("Write your recommendation...")
    if st.button("Submit Recommendation"):
        st.success("Recommendation submitted!")

# Footer
st.sidebar.write("Developed using Streamlit")
