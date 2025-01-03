import streamlit as st
import pandas as pd
import requests
from datetime import datetime

API_URL = "http://localhost:8000"  # Replace with your actual API URL

def analytics_months_tab():
    # Define two columns for date input fields
    col1, col2 = st.columns(2)

    with col1:
        start_date_2 = st.date_input("Start Date", datetime(2024, 8, 1), key="start_date")
    with col2:
        end_date_2 = st.date_input("End Date", datetime(2024, 8, 5), key="end_date")

    # Button to trigger API call
    if st.button("Get Analytics Months"):
        # Construct payload for the API
        payload = {
            "start_date": start_date_2.strftime("%Y-%m-%d"),
            "end_date": end_date_2.strftime("%Y-%m-%d")
        }

        try:
            # Make a POST request to the API
            response = requests.post(f"{API_URL}/analytics_months/", json=payload)
            response.raise_for_status()  # Raise an error for HTTP issues
            data = response.json()

            # Process the API response into a DataFrame
            data_month = {
                "Month": list(data.keys()),
                "Month Name": [data[month]["Month Name"] for month in data],
                "Total": [data[month]["Total"] for month in data]
            }
            df2 = pd.DataFrame(data_month)

            # Format 'Total' and set 'Month' as the index
            df2['Total'] = df2['Total'].astype(int)  # Convert 'Total' to integer
            df2.set_index('Month', inplace=True)  # Set 'Month' as the index

            # Sort the DataFrame by 'Month'
            df_sorted_2 = df2.sort_values(by="Month", ascending=True)

            # Display the analytics
            st.title("Expense Breakdown By Month")
            st.bar_chart(data=df_sorted_2.set_index("Month Name")['Total'], use_container_width=True)
            st.table(df_sorted_2)

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data from API: {e}")
        except KeyError as e:
            st.error(f"Unexpected data format from API. Missing key: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
