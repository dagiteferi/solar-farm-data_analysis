import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator
import os

# Check the current working directory and list files
st.write("Current working directory:", os.getcwd())
st.write("Files in directory:", os.listdir())

# Set the background color and theme
st.set_page_config(page_title="Solar Panel Installation Comparison", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #001f3f;
    }
    .stApp {
        background-color: #001f3f;
    }
    .stSelectbox, .stRadio {
        color: #ffffff;
        background-color: #004080;
        border-radius: 8px;
    }
    h1, h2, h3, h4, h5, h6, .stText {
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Solar Panel Installation Comparison")

# Load your data with correct paths
data_benin = pd.read_csv(r'C:\Users\Dagi\Documents\KAIM\week 0\solar-farm-data_analysis\data\benin-malanville.csv', parse_dates=['Timestamp'])
data_togo = pd.read_csv(r'C:\Users\Dagi\Documents\KAIM\week 0\solar-farm-data_analysis\data\togo-dapaong_qc.csv', parse_dates=['Timestamp'])
data_sierra_leone = pd.read_csv(r'C:\Users\Dagi\Documents\KAIM\week 0\solar-farm-data_analysis\data\sierraleone-bumbuna.csv', parse_dates=['Timestamp'])

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
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.patch.set_facecolor('#00264d')  # Set figure background color
    for ax in axs.flat:
        ax.set_facecolor('#001f3f')  # Set axes background color
        ax.grid(True, color='#004080')  # Set grid color
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))  # Date format for x-axis
        ax.xaxis.set_major_locator(MaxNLocator(integer=True, prune='both'))

    # Plot GHI
    axs[0, 0].plot(filtered_data['GHI'], label='GHI', color='#00FFFF', linewidth=2)  # Cyan
    axs[0, 0].set_title('GHI (Global Horizontal Irradiance)', color='white')
    axs[0, 0].set_xlabel('Time', color='white')
    axs[0, 0].set_ylabel('GHI', color='white')
    axs[0, 0].tick_params(axis='x', colors='white', rotation=45)
    axs[0, 0].tick_params(axis='y', colors='white')

    # Plot DNI
    axs[0, 1].plot(filtered_data['DNI'], label='DNI', color='#FF00FF', linewidth=2)  # Magenta
    axs[0, 1].set_title('DNI (Direct Normal Irradiance)', color='white')
    axs[0, 1].set_xlabel('Time', color='white')
    axs[0, 1].set_ylabel('DNI', color='white')
    axs[0, 1].tick_params(axis='x', colors='white', rotation=45)
    axs[0, 1].tick_params(axis='y', colors='white')

    # Plot DHI
    axs[1, 0].plot(filtered_data['DHI'], label='DHI', color='#32CD32', linewidth=2)  # Lime Green
    axs[1, 0].set_title('DHI (Diffuse Horizontal Irradiance)', color='white')
    axs[1, 0].set_xlabel('Time', color='white')
    axs[1, 0].set_ylabel('DHI', color='white')
    axs[1, 0].tick_params(axis='x', colors='white', rotation=45)
    axs[1, 0].tick_params(axis='y', colors='white')

    # Plot Tamb (Ambient Temperature)
    axs[1, 1].plot(filtered_data['Tamb'], label='Tamb', color='#FF7F50', linewidth=2)  # Coral
    axs[1, 1].set_title('Tamb (Ambient Temperature)', color='white')
    axs[1, 1].set_xlabel('Time', color='white')
    axs[1, 1].set_ylabel('Temperature (°C)', color='white')
    axs[1, 1].tick_params(axis='x', colors='white', rotation=45)
    axs[1, 1].tick_params(axis='y', colors='white')

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
