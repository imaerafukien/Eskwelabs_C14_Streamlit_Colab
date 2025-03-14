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
    st.write("This is an overview of the project.")

    # Display an image from images folder
    #overall_img_path = os.path.join(image_dir, "logo.png")
    #if os.path.exists(overall_img_path):
        #st.image(overall_img_path, caption="Project Overview", use_container_width=True)
    #else:
        #st.warning("No overview image found. Please add an image to `images/` directory.")

    # create plot of 2020 transaction count vs 2021 transaction count of df by month using 3 letters for the month
    df['trans_datetime'] = pd.to_datetime(df['trans_datetime'])
    df['trans_year'] = df['trans_datetime'].dt.year
    df['trans_month'] = df['trans_datetime'].dt.month
    df['trans_month'] = df['trans_month'].apply(lambda x: x[:3])
    df_2020 = df[df['trans_year'] == 2020]
    df_2021 = df[df['trans_year'] == 2021]
    df_2020_count = df_2020.groupby('trans_month')['trans_num'].count()
    df_2021_count = df_2021.groupby('trans_month')['trans_num'].count()
    df_2020_count.plot(kind='bar', label='2020')
    df_2021_count.plot(kind='bar', label='2021')
    plt.legend()
    plt.xlabel('Month')
    plt.ylabel('Transaction Count')
    plt.title('2020 vs 2021 Transaction Count by Month')
    plt.savefig(os.path.join(plot_dir, 'transaction_count_by_month.png'))
    st.pyplot(plt)

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
