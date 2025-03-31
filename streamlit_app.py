import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from datetime import datetime

# Create a title for the app
st.title("Interactive Data Visualization")

# Sample data generation function
def generate_sample_data():
    x = np.linspace(0, 10, 50)
    sine = np.sin(x)
    cosine = np.cos(x)
    tangent = np.clip(np.tan(x), -10, 10)  # Clamp values
    
    return pd.DataFrame({
        'X': x,
        'Sine Wave': sine,
        'Cosine Wave': cosine,
        'Tangent Wave': tangent
    })

# Sidebar controls
st.sidebar.header("Data Source")
data_source = st.sidebar.radio(
    "Select data source:",
    ["Sample Data", "Upload CSV", "API Data"]
)

# Handle different data sources
if data_source == "Sample Data":
    data = generate_sample_data()
    st.write("### Using sample data")
    
elif data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            st.write("### Using uploaded CSV data")
        except Exception as e:
            st.error(f"Error: {e}")
            data = generate_sample_data()
    else:
        st.sidebar.info("Please upload a CSV file")
        data = generate_sample_data()
        
elif data_source == "API Data":
    api_options = ["Stock Market", "Weather Data", "COVID-19 Data"]
    api_choice = st.sidebar.selectbox("Select API source:", api_options)
    
    if api_choice == "Stock Market":
        symbol = st.sidebar.text_input("Stock Symbol", "MSFT")
        st.sidebar.info("Using demo API key")
        if st.sidebar.button("Fetch Data"):
            try:
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey=demo"
                r = requests.get(url)
                json_data = r.json()
                
                # Extract and convert time series data
                time_series = json_data.get("Time Series (Daily)", {})
                records = []
                for date, values in time_series.items():
                    record = {"Date": date}
                    record.update({k.split(". ")[1]: float(v) for k, v in values.items()})
                    records.append(record)
                
                data = pd.DataFrame(records)
                if not data.empty:
                    data['Date'] = pd.to_datetime(data['Date'])
                    data = data.sort_values('Date')
                else:
                    st.error("No data retrieved")
                    data = generate_sample_data()
            except Exception as e:
                st.error(f"Error fetching data: {e}")
                data = generate_sample_data()
        else:
            # Default data before fetching
            data = generate_sample_data()
    else:
        st.sidebar.info("This API is not implemented in this demo")
        data = generate_sample_data()

# Display the data
st.write("### Data Preview:")
st.dataframe(data.head(10))

# Visualization options
st.sidebar.header("Visualization")
chart_type = st.sidebar.selectbox(
    "Select chart type:",
    ["Line Chart", "Bar Chart", "Scatter Plot", "Area Chart"]
)

# Let user select columns for visualization
if not data.empty:
    # Get numeric columns for y-axis
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    # Get all columns for x-axis
    all_cols = data.columns.tolist()
    
    # Column selection
    x_column = st.sidebar.selectbox("Select X-axis column", all_cols)
    y_columns = st.sidebar.multiselect("Select Y-axis column(s)", numeric_cols, default=[numeric_cols[0]] if numeric_cols else [])
    
    if x_column and y_columns:
        st.write(f"### {chart_type}")
        
        # Create the appropriate chart
        if chart_type == "Line Chart":
            fig = px.line(data, x=x_column, y=y_columns, title=f"{', '.join(y_columns)} over {x_column}")
        elif chart_type == "Bar Chart":
            fig = px.bar(data, x=x_column, y=y_columns, title=f"{', '.join(y_columns)} by {x_column}")
        elif chart_type == "Scatter Plot":
            fig = px.scatter(data, x=x_column, y=y_columns[0] if y_columns else None, 
                            title=f"{y_columns[0] if y_columns else ''} vs {x_column}")
        elif chart_type == "Area Chart":
            fig = px.area(data, x=x_column, y=y_columns, title=f"{', '.join(y_columns)} over {x_column}")
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please select columns for both axes")
else:
    st.error("No data available for visualization")

# Add download option
if not data.empty:
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    ) 