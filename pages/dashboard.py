import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
def load_data():
    folder_path = "/raw_data/"
    file_name = "all_expanded_UI.csv"
    file_path = os.path.join(os.getcwd() + folder_path, file_name)
    df = pd.read_csv(file_path)
    return df

df = load_data()

# Sidebar for Filters
st.sidebar.header("Filters")

# Dropdown for Year in Sidebar
unique_years = sorted(df['Ano'].unique())
selected_year = st.sidebar.selectbox('Select Year:', unique_years)

# Dropdown for State in Sidebar
# unique_states = sorted(df['Estado'].unique())
# selected_state = st.sidebar.selectbox('Select State:', unique_states)

# Dropdown for State in Sidebar, excluding "Distrito Federal"
unique_states = sorted([state for state in df['Estado'].unique() if state != 'Distrito Federal'])
selected_state = st.sidebar.selectbox('Select State:', unique_states)


# Dropdown for Features in Sidebar
features = ['Aprovação', 'Reprovação', 'Abandono', 'Matrículas', 'Docentes']
selected_feature = st.sidebar.selectbox('Select Feature:', features)

# Filter and sort data
filtered_df = df[(df['Ano'] == selected_year) & (df['Estado'] == selected_state)]
sorted_df = filtered_df.groupby('Município')[selected_feature].mean().sort_values(ascending=False).reset_index().head(10)

# Update the site title dynamically
st.title(f"Top 10 Municipalities by {selected_feature} for {selected_year} in {selected_state}")

# Display the chart with reduced size
fig, ax = plt.subplots(figsize=(8, 4))  # Reduced width and height
sns.barplot(x=selected_feature, y='Município', data=sorted_df, ax=ax, linewidth=0)

# Remove the spines (chart border)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Remove X and Y labels
ax.set_xlabel('')
ax.set_ylabel('')

st.pyplot(fig)
