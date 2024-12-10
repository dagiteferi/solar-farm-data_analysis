import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator
import os

# Set the background color and theme
st.set_page_config(page_title="Solar Panel Installation Comparison", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
    }
    .stApp {
        background-color: #f5f5f5;
    }
    .stSelectbox, .stRadio {
        color: #000000 !important;
        background-color: #ffffff;
        border: 1px solid #dddddd;
        border-radius: 8px;
        padding: 5px;
    }
    .stRadio > div > label {
        color: #000000 !important;
    }
    h1, h2, h3, h4, h5, h6, .stText {
        color: #333333;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        margin: 10px 0;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Solar Panel Installation Comparison")

# Load your data with correct paths
data_path = r'C:\Users\Dagi\Documents\KAIM\week 0\solar-farm-data_analysis\data'
data_benin = pd.read_csv(f'{data_path}\\benin-malanville.csv', parse_dates=['Timestamp'])
data_togo = pd.read_csv(f'{data_path}\\togo-dapaong_qc.csv', parse_dates=['Timestamp'])
data_sierra_leone = pd.read_csv(f'{data_path}\\sierraleone-bumbuna.csv', parse_dates=['Timestamp'])

# Create radio buttons for country selection
country = st.radio("Select a country:", ['Benin', 'Togo', 'Sierra Leone'])

# Define a function to filter data based on frequency
def filter_data(data, freq):
    if freq == 'Daily':
        return data.resample('D', on='Timestamp').mean()
    elif freq == 'Monthly':
        return data.resample('M', on='Timestamp').mean()
    elif freq == 'Quarterly':
        return data.resample('Q', on='Timestamp').mean()
    else:
        return data

# Define a function to create and display plots
def plot_solar_data(data, country_name, freq):
    # Filter the data based on the selected frequency
    filtered_data = filter_data(data, freq)

    st.subheader(f"{country_name} Solar Data ({freq})")
    st.write(filtered_data.head())

    # Set figure and axes background color
    fig, axs = plt.subplots(2, 2, figsize=(14, 10), facecolor='#f5f5f5')
    for ax in axs.flat:
        ax.set_facecolor('#ffffff')
        ax.grid(True, color='#dddddd')
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(MaxNLocator(integer=True, prune='both'))

    # Plot GHI
    axs[0, 0].plot(filtered_data['GHI'], label='GHI', color='#FF6347', linewidth=2)  # Tomato
    axs[0, 0].set_title('GHI (Global Horizontal Irradiance)', color='#333333')
    axs[0, 0].set_xlabel('Time', color='#333333')
    axs[0, 0].set_ylabel('GHI', color='#333333')
    axs[0, 0].tick_params(axis='x', colors='#333333', rotation=45)
    axs[0, 0].tick_params(axis='y', colors='#333333')

    # Plot DNI
    axs[0, 1].plot(filtered_data['DNI'], label='DNI', color='#4682B4', linewidth=2)  # SteelBlue
    axs[0, 1].set_title('DNI (Direct Normal Irradiance)', color='#333333')
    axs[0, 1].set_xlabel('Time', color='#333333')
    axs[0, 1].set_ylabel('DNI', color='#333333')
    axs[0, 1].tick_params(axis='x', colors='#333333', rotation=45)
    axs[0, 1].tick_params(axis='y', colors='#333333')

    # Plot DHI
    axs[1, 0].plot(filtered_data['DHI'], label='DHI', color='#32CD32', linewidth=2)  # Lime Green
    axs[1, 0].set_title('DHI (Diffuse Horizontal Irradiance)', color='#333333')
    axs[1, 0].set_xlabel('Time', color='#333333')
    axs[1, 0].set_ylabel('DHI', color='#333333')
    axs[1, 0].tick_params(axis='x', colors='#333333', rotation=45)
    axs[1, 0].tick_params(axis='y', colors='#333333')

    # Plot Tamb (Ambient Temperature)
    axs[1, 1].plot(filtered_data['Tamb'], label='Tamb', color='#FFA07A', linewidth=2)  # Light Salmon
    axs[1, 1].set_title('Tamb (Ambient Temperature)', color='#333333')
    axs[1, 1].set_xlabel('Time', color='#333333')
    axs[1, 1].set_ylabel('Temperature (°C)', color='#333333')
    axs[1, 1].tick_params(axis='x', colors='#333333', rotation=45)
    axs[1, 1].tick_params(axis='y', colors='#333333')

    # Adjust layout and display
    plt.tight_layout()
    st.pyplot(fig)

# Create a dropdown for selecting frequency
freq = st.selectbox("Select frequency:", ['Daily', 'Monthly', 'Quarterly'])

# Display data and charts based on the selected country and frequency
if country == 'Benin':
    plot_solar_data(data_benin, "Benin", freq)
elif country == 'Togo':
    plot_solar_data(data_togo, "Togo", freq)
elif country == 'Sierra Leone':
    plot_solar_data(data_sierra_leone, "Sierra Leone", freq)
