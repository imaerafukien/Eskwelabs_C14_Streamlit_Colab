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
    df = pd.read_csv('data/cc_clean.csv')
    # create plot of 2020 transaction count vs 2021 transaction count of df by month, convert month number to 3 letters for the plot
    df['trans_month'] = df['trans_month'].map({1: 'Jan', 2: 'Feb', 3: 'Mar',
                                               4: 'Apr', 5: 'May', 6: 'Jun',
                                               7: 'Jul', 8: 'Aug', 9: 'Sep',
                                               10: 'Oct', 11: 'Nov', 12: 'Dec'})
    df_2020 = df[df['trans_year'] == 2020]
    df_2021 = df[df['trans_year'] == 2021]
    df_2020 = df_2020.groupby('trans_month')['trans_num'].count()
    df_2021 = df_2021.groupby('trans_month')['trans_num'].count()
    df_2020.plot(kind='bar', label='2020')
    df_2021.plot(kind='bar', label='2021')
    plt.legend()
    plt.title('Transaction Count by Month')
    plt.xlabel('Month')
    plt.ylabel('Transaction Count')
    plt.savefig('plots/transaction_count_by_month.png')
    st.image('plots/transaction_count_by_month.png')



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
