import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import altair as alt

# Set page title
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Overall", "Introduction", "Methodology", "Scope & Limitations","Results", "Proof of Concept"])

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
    st.write("We aim to know who Adobo Bank's customers are, what the bank's current data quality is, how to improve data gathering and from their current set of data, how we can contribute to Adobo Bank's growth.")


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
    # generate bar graph showing acct_num count by generation using alt
    st.subheader("Demographic Profile of Adobo Bank Customers")
    gen_counts = rfm_df['generation'].value_counts().reset_index()
    gen_counts.columns = ['generation', 'account_count']

    # Create Altair bar graph
    chart = alt.Chart(gen_counts).mark_bar().encode(
        x=alt.X('generation:N', title='Generation', sort=['Greatest', 'Silent', 'Baby Boomer', 'Gen X'], axis=alt.Axis(labelAngle=0)),
        y=alt.Y('account_count:Q', title='Number of Accounts'),
        tooltip=['generation', 'account_count']  # Optional: show details on hover
    ).properties(
        width=500,
        height=400,
        title='Account Distribution by Generation'
    )
    st.altair_chart(chart, use_container_width=True)
    st.write("Population Age Mean: ", rfm_df['age'].mean().round(2))
    st.write("Population Age Min: ", rfm_df['age'].min())
    st.write("Population Age Max: ", rfm_df['age'].max())
    st.caption("Out of 88 unique customers, majority of Adobo Bank Customers belong in the Baby Boomer Generation (52 customers). ")
    st.caption("All of Adobo Bank's customers are over 52 years old")
    st.divider()
    # create a horizontal bar graph of value_counts of category_group in df, sort highest to lowest
    st.subheader("Customer Total Transaction Counts per Category")
    counts_df = df['category_group'].value_counts().reset_index()
    counts_df.columns = ['category_group', 'count']
    chart = alt.Chart(counts_df).mark_bar().encode(
    x=alt.X('count:Q', title='Transaction Count'),
    y=alt.Y('category_group:N', sort='-x', title='Category Group'),
    tooltip=['category_group', 'count']
    ).properties(
    width=600,
    height=400
    )
    st.altair_chart(chart, use_container_width=True)
    st.caption("Most transactions are in the shopping & micellaneous category followed by home & family tied with food & essentials")
    st.divider()
    # create a horizontal bar chart of sum of 'amt' per 'category_group' in df sorted highest to lowest using alt
    st.subheader("Customer Total Transaction Amounts per Category")
    amt_df = df.groupby('category_group')['amt'].sum().reset_index()
    amt_df.columns = ['category_group', 'amt']
    chart = alt.Chart(amt_df).mark_bar().encode(
    x=alt.X('amt:Q', title='Total Transaction Amount'),
    y=alt.Y('category_group:N', sort='-x', title='Category Group'),
    tooltip=['category_group', 'amt']
    ).properties(
    width=600,
    height=400
    )
    st.altair_chart(chart, use_container_width=True)
    st.caption("Most transactions are in the shopping & micellaneous category followed by food & essentials, then by home & family category")
    st.divider()
    # create line chart of 'trans_num' count by month for year 2020 and 2021 with Jan - Dec on the x-axis and 'trans_num' count on the y-axis, use alt
    st.subheader("Customer Transaction Count per Year")
    df['trans_date'] = pd.to_datetime(df['trans_datetime'])
    df['year'] = df['trans_date'].dt.year
    df['month'] = df['trans_date'].dt.month

    # Filter and aggregate
    df_2020 = df[df['year'] == 2020].groupby('month')['trans_num'].count().reset_index()
    df_2021 = df[df['year'] == 2021].groupby('month')['trans_num'].count().reset_index()
    df_2020['year'] = 2020
    df_2021['year'] = 2021
    df_2020.columns = ['month', 'trans_count', 'year']
    df_2021.columns = ['month', 'trans_count', 'year']

    # Ensure all months are present
    all_months = pd.DataFrame({'month': range(1, 13)})
    df_2020_full = all_months.merge(df_2020, on='month', how='left').fillna({'trans_count': 0})
    df_2021_full = all_months.merge(df_2021, on='month', how='left').fillna({'trans_count': 0})
    df_2020_full['year'] = 2020
    df_2021_full['year'] = 2021

    # Combine data
    df_2020_2021 = pd.concat([df_2020_full, df_2021_full])

    # Add month names
    month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    df_2020_2021['month_name'] = df_2020_2021['month'].map(month_map)

    # Debug data
    #st.write("Final df_2020_2021:")
    #st.write(df_2020_2021)

    # Ensure data types
    df_2020_2021['trans_count'] = df_2020_2021['trans_count'].astype(int)
    df_2020_2021['year'] = df_2020_2021['year'].astype(str)

    # Create line chart with explicit layering for each year
    base = alt.Chart(df_2020_2021).encode(
        x=alt.X('month_name:N', 
                title='Month', 
                sort=list(month_map.values()), 
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('trans_count:Q', title='Transaction Count'),
        tooltip=['month_name', 'trans_count', 'year']
    )

    line = base.mark_line(point=True).encode(
        color=alt.Color('year:N', 
                        title='Year', 
                        scale=alt.Scale(domain=['2020', '2021'], range=['#1f77b4', '#ff7f0e']))
    ).properties(
        width=600,
        height=400,
        title='Transaction Counts by Month (2020-2021)'
    )

    # Display chart
    st.altair_chart(line, use_container_width=True)
    st.caption("December 2021 data is cut short at Dec 8 which could be the reason for the sudden drop")
    st.caption("There is clear seasonality in spending behavior")
    st.divider()
    st.subheader("Total Amount Spent per Month (2020-2021)")
    df['trans_date'] = pd.to_datetime(df['trans_datetime'])
    df['year'] = df['trans_date'].dt.year
    df['month'] = df['trans_date'].dt.month

    # Filter and aggregate total 'amt' per month
    df_2020 = df[df['year'] == 2020].groupby('month')['amt'].sum().reset_index()
    df_2021 = df[df['year'] == 2021].groupby('month')['amt'].sum().reset_index()
    df_2020['year'] = 2020
    df_2021['year'] = 2021
    df_2020.columns = ['month', 'total_amt', 'year']
    df_2021.columns = ['month', 'total_amt', 'year']

    # Ensure all months are present
    all_months = pd.DataFrame({'month': range(1, 13)})
    df_2020_full = all_months.merge(df_2020, on='month', how='left').fillna({'total_amt': 0})
    df_2021_full = all_months.merge(df_2021, on='month', how='left').fillna({'total_amt': 0})
    df_2020_full['year'] = 2020
    df_2021_full['year'] = 2021

    # Combine data
    df_2020_2021 = pd.concat([df_2020_full, df_2021_full])

    # Add month names
    month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    df_2020_2021['month_name'] = df_2020_2021['month'].map(month_map)

    # Debug data
    #st.write("Final df_2020_2021:")
    #st.write(df_2020_2021)

    # Ensure data types
    df_2020_2021['total_amt'] = df_2020_2021['total_amt'].astype(float)  # Keep as float for decimals
    df_2020_2021['year'] = df_2020_2021['year'].astype(str)

    # Create line chart
    base = alt.Chart(df_2020_2021).encode(
        x=alt.X('month_name:N', 
                title='Month', 
                sort=list(month_map.values()), 
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('total_amt:Q', title='Total Amount Spent'),
        tooltip=['month_name', 'total_amt', 'year']
    )

    line = base.mark_line(point=True).encode(
        color=alt.Color('year:N', 
                        title='Year', 
                        scale=alt.Scale(domain=['2020', '2021'], range=['#1f77b4', '#ff7f0e']))
    ).properties(
        width=600,
        height=400,
        title='Total Amount Spent by Month (2020-2021)'
    )

    # Display chart
    st.altair_chart(line, use_container_width=True)
    st.caption("December 2021 data is cut short at Dec 8 which could be the reason for the sudden drop")
    st.caption("There is clear seasonality in spending behavior")
    st.divider()

    # Create visualization for the k means clustering
    st.subheader("Customer Segmentation")
    st.write("We segmented our customers using the k means clustering algorithm")
    st.caption("Only numerical features were used for clustering: recency, frequency, total_amt, avg_spend, tenure, clv, city_pop ")
    cluster_means = rfm_df.groupby('labels_rfm_clustering')[["recency", "frequency", "total_amt", 
                                                         "avg_spend", "tenure", "clv", "city_pop"]].mean().reset_index()
    st.write(cluster_means)
    # Normalize means to 0-1, inverting recency
    metrics = ["recency", "frequency", "total_amt", "avg_spend", "tenure", "clv", "city_pop"]
    for col in metrics:
        if col == "recency":
            # Invert recency: higher normalized value = more recent (lower raw value)
            cluster_means[col] = (cluster_means[col].max() - cluster_means[col]) / (cluster_means[col].max() - cluster_means[col].min())
        else:
            # Standard normalization: higher raw value = higher normalized value
            cluster_means[col] = (cluster_means[col] - cluster_means[col].min()) / (cluster_means[col].max() - cluster_means[col].min())

    # Melt to long format
    cluster_means_long = cluster_means.melt(id_vars=['labels_rfm_clustering'], 
                                            value_vars=metrics,
                                            var_name='metric', 
                                            value_name='normalized_mean')

    # Create faceted bar chart with narrower bars
    chart = alt.Chart(cluster_means_long).mark_bar(size=20).encode(
        x=alt.X('labels_rfm_clustering:N', title='Cluster Label'),
        y=alt.Y('normalized_mean:Q', title='Normalized Mean (0-1)', scale=alt.Scale(domain=[0, 1])),
        color=alt.Color('labels_rfm_clustering:N', title='Cluster'),
        column=alt.Column('metric:N', title='Metric', 
                          sort=['recency', 'frequency', 'total_amt', 'avg_spend', "tenure", "clv", "city_pop"])
    ).properties(
        width=160,  # Narrow facet width
        height=300,
        title='Normalized Mean Metrics by Cluster (Recency Inverted)'
    ).configure_axis(
        labelAngle=0  # Horizontal labels
    )
    # Display in Streamlit with fixed width
    st.subheader("K-Means Clustering: Mean Metrics by Cluster (Inverted Recency)")
    st.altair_chart(chart, use_container_width=False)
    st.caption("Recency was inverted for a more intuitive viewing of the data where higher values are better")
    # Debug: Show the data
    #st.write("Cluster Means (Normalized, Recency Inverted):")
    #st.write(cluster_means_long)
    st.divider()
    st.subheader("Cluster Analysis")
    st.write("We labeled each cluster according to their spending habit")
    data = {
    'Cluster Label': ['Smart Essentials Spender', 'Luxury Essentials Enthusiast', 'Premium Shopper & Leisure Seeker'],
    'Recency': ['Frequent purchases', 'Very frequent purchases', 'Infrequent purchases'],
    'Frequency': ['High transactions', 'Very high transactions', 'Low transactions'],
    'Total Amount Spent': ['Moderate spend', 'High spend', 'Lower total, high per transaction'],
    'Avg. Spending per Transaction': ['Low spend per transaction', 'Moderate spend per transaction', 'Very high spend per transaction'],
    'Tenure': ['Long tenure', 'Very long tenure', 'Shorter tenure'],
    'Customer Lifetime Value': ['Moderate CLV', 'High CLV', 'Low CLV'],
    'City Population': ['Large cities', 'Mid-sized cities', 'Mid-sized cities']
    }


    # Create DataFrame with string descriptions
    rfm_df_string = pd.DataFrame(data)
    rfm_df_string.iloc[[0,1]] = rfm_df_string.iloc[[1,0]]
    rfm_df_string.iloc[[1,2]] = rfm_df_string.iloc[[2,1]]
    st.table(rfm_df_string)
    st.subheader("Credit Card Expansion Recommendation")
    st.info("**Smart Essentials Spender (Elite Rewards Card)**  \nFrequent spender on everyday necessities, values cashback and rewards for recurring purchases. Best suited for individuals who optimize spending for long-term savings and rewards.")
    st.info("**Luxury Essentials Enthusiast (Gold Lifestyle Card)**  \nHigh-frequency spender who prioritizes premium experiences while maintaining practical spending habits. Prefers a mix of luxury and everyday purchases, benefiting from exclusive perks & travel rewards.")
    st.info("**Premium Shopper & Leisure Seeker (Signature Luxe Card)**  \nSelective, high-value spender focused on luxury shopping, travel, and exclusive experiences. This customer prioritizes premium memberships, concierge services, and elite shopping benefits.")
  

# Proof of Concept Section
elif menu == "Proof of Concept":
    st.title("Proof of Concept")
    st.subheader("How can Adobo Bank effectively tailor its expanded credit card offerings to better serve its customers?")
    st.write("Develop a system that efficiently provides personalized credit card recommendations to customers based on their financial profile, spending habits, and the bank’s customer segmentation framework.")
    st.divider()
    st.subheader("Personalized Credit Card Recommendation Model")
    st.info("**Objective**  \nDevelop a system for personalized credit card recommendations based on customers' financial profiles & spending habits.")
    st.info("**Approach**  \nUse regression analysis to match customers with the best credit card options.")
    st.info("**Channels**  \nAdobo Bank App & Website: New and existing customers can enter their income and spending habits to receive personalized credit card recommendations instantly.")
    st.info("**Benefits**  \nProvide clear credit card options upfront, minimizing consultation time and accelerating customer acquisition.")
    st.divider()
    st.subheader("Credit Card Recommendation System")
    st.markdown("- **User Input**  \nCustomers enter income and spending habits via the app or website.")
    st.markdown("- **Data Processing**  \nThe system processes customer data using regression model.")
    st.markdown("- **Tailored Recommendation**  \nBest credit card options are suggested.")
    st.markdown("- **Application Next Steps**  \nCustomers can apply immediately or request a callback.")
    st.divider()
    st.subheader("Machine Learning Classification Model")
    st.info(
    "<h3 style='text-align: center;'>Personalized Credit Card Type Recommendations</h3>",
    unsafe_allow_html=True
    )
    with st.expander("**Demographic Profile**"):
      st.write("age, age group/ generation, date of birth, home address/ transaction location")
    with st.expander("**Financial Profile**"):
      st.write("occupation, monthly income, assets, liabilities")
    with st.expander("**Spending Habits**"):
      st.write("transaction recency, tenure & frequency, amount spending, transaction categories, customer lifetime value")
    with st.expander("**Customer Segmentation**"):
      st.write("Identify best customer segment through regression model")


# Footer
st.sidebar.write("Developed using Streamlit")
