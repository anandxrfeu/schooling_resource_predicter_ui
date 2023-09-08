import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import folium_static
import matplotlib
import matplotlib.pyplot as plt

# Load the dataset
def load_data():
    folder_path = "/raw_data/"
    file_name = "all_expanded_UI.csv"
    file_path = os.path.join(os.getcwd() + folder_path, file_name)
    df = pd.read_csv(file_path)
    return df

df = load_data()

# Define the list of features that can be selected for the heatmap
feature_list = [
    'Aprovação', 'Reprovação', 'Abandono', 'Matrículas',
    'Docentes', 'Estabelecimentos', 'Turmas', 'Adjusted_population',
    'Adjusted_funding'
]

# Sidebar for Filters
st.sidebar.header("Filters")

# Dropdown for Year in Sidebar
unique_years = sorted(df['Ano'].unique())
selected_year = st.sidebar.selectbox("Select Year", unique_years)

# Dropdown for Feature in Sidebar
feature_list = ['Aprovação', 'Reprovação', 'Abandono', 'Matrículas', 'Docentes', 'Estabelecimentos', 'Turmas', 'Adjusted_population', 'Adjusted_funding']
selected_feature = st.sidebar.selectbox("Select Feature", feature_list)

# Title
st.title(f"Municipality {selected_feature} Heatmap")

# Filter the data based on selected Year and Feature
df_filtered = df[df['Ano'] == selected_year]

# Identify min and max values for the selected feature
min_value = df_filtered[selected_feature].min()
max_value = df_filtered[selected_feature].max()

# Color normalization
norm = matplotlib.colors.Normalize(vmin=min_value, vmax=max_value)

# Create the Heatmap
m = folium.Map(location=[-15.788497, -47.879873], zoom_start=4)

for idx, row in df_filtered.iterrows():
    scaled_radius = (row[selected_feature] - min_value) / (max_value - min_value) * 10 + 1  # Scale the radius
    color = plt.cm.viridis(norm(row[selected_feature]))  # Get color from color map
    folium.CircleMarker(location=[row['Latitude'], row['Longitude']],
                        radius=scaled_radius,
                        color=matplotlib.colors.rgb2hex(color),
                        fill=True,
                        fill_color=matplotlib.colors.rgb2hex(color),
                        fill_opacity=0.6,
                        popup=f"{row['Município']} ({row['Localização']}): {row[selected_feature]}").add_to(m)

folium_static(m)
