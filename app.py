from dotenv import load_dotenv

import os

import pandas as pd
import numpy as np

import streamlit as st
import plotly.express as px
import requests

# Load .env file
load_dotenv()




st.set_page_config(layout="wide", page_title="Education Resource Predictor")

# Function to format numbers to "Millions"
def format_to_millions(number):
    return round((number / 1_000_000), 2)

def get_prediction_data(ibge_code, year=2023, passing_rate=99, localization='Urbana'):

    params = {
        "year" : year,
        "passing_rate": passing_rate,
        "localization": localization
    }
    #ibge_code = 1100015
    response = requests.get(f'{os.environ.get("API_URL")}{ibge_code}', params=params)

    try:
        if response.status_code == 200:
            resonse_data = response.json()
            funding_df = pd.DataFrame(resonse_data.pop("Historic_funding"))
            funding_df.rename(columns={'Ano': 'Year', 'Adjusted_funding': 'Funding (R$)'}, inplace=True)
            funding_df['Funding (R$)'] = funding_df['Funding (R$)'].apply(format_to_millions)
            funding_df['Status'] = ['Actual' if year < 2023 else 'Predicted' for year in funding_df['Year']]
            municipality_data = resonse_data
            return municipality_data, funding_df
    except Exception as e:
        print(e)
        return {}, pd.DataFrame()

def center_and_bold_text(text):
    return f"<div style='text-align: center; font-weight: bold;'>{text}</div>"

def center_text(text):
    return f"<div style='text-align: center; '>{text}</div>"

def left_justify(text):
    return f"<div style='padding: 15px; line-height:0px;'>{text}</div>"

########################################################################
# UI
########################################################################

########################### Sidebar

#[1100015, 3151602, 4127601]
municipality = st.sidebar.selectbox("**Choose a municipality:**",(1100015, 3151602, 4127601))

st.sidebar.markdown(
    """
**Prediction parameters:**
"""
)

year = st.sidebar.slider(
    "Year", min_value=2022, max_value=2025, value=2023, step=1
)
passing_rate = st.sidebar.slider(
    "Passing Rate", min_value=80, max_value=99, value=85, step=5
)

localization  = st.sidebar.radio(
    "Localization",
    ["Urban", "Rural"], horizontal=True)


municipality_data, funding_data = get_prediction_data(municipality, year)

# st.sidebar.markdown(
#     f"""
# **Other parameters (circa 2020):**

#     Population {municipality_data["Adjusted_population"]}
#     GDP per capita R${municipality_data["PIB"]}
#     Poverty {municipality_data["Poverty_%"]}%
#     Malnutrition {municipality_data["Magreza_total_%"]}%
#     Internet Access {municipality_data["Acesso_a_internet_%"]}%
# """
# )

st.sidebar.markdown(f"""**Other parameters (circa 2020):**""", unsafe_allow_html=True)
st.sidebar.markdown(left_justify(f"""Population {municipality_data["Adjusted_population"]}"""), unsafe_allow_html=True)
st.sidebar.markdown(left_justify(f"""GDP per capita R$ {municipality_data["PIB"]}"""), unsafe_allow_html=True)
st.sidebar.markdown(left_justify(f"""Poverty{municipality_data["Poverty_%"]}%"""), unsafe_allow_html=True)
st.sidebar.markdown(left_justify(f"""Malnutrition {municipality_data["Magreza_total_%"]}%"""), unsafe_allow_html=True)
st.sidebar.markdown(left_justify(f"""Internet Access {municipality_data["Acesso_a_internet_%"]}%"""), unsafe_allow_html=True)


########################### Main panel

st.title(f"Funding needs for {municipality}")
st.markdown("<br>", unsafe_allow_html=True)


student_teacher_ratio = round(int(municipality_data["Matrículas"]) / int(municipality_data["Docentes"]),2)


if municipality_data:
    # Create layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(center_and_bold_text("Passing Rate"), unsafe_allow_html=True)
        st.markdown(center_text(municipality_data["Aprovação"]), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        #st.divider()

        st.markdown(center_and_bold_text("Schools"), unsafe_allow_html=True)
        st.markdown(center_text(municipality_data["Estabelecimentos"]), unsafe_allow_html=True)
        #st.divider()


    with col2:
        st.markdown(center_and_bold_text("Failling Rate"), unsafe_allow_html=True)
        st.markdown(center_text(municipality_data["Reprovação"]), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        #st.divider()


        st.markdown(center_and_bold_text("Enrolments"), unsafe_allow_html=True)
        st.markdown(center_text(municipality_data["Matrículas"]), unsafe_allow_html=True)
        #st.divider()


    with col3:
        st.markdown(center_and_bold_text("Dropout Rate"), unsafe_allow_html=True)
        st.markdown(center_text(municipality_data["Abandono"]), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        #st.divider()

        st.markdown(center_and_bold_text("Batches"), unsafe_allow_html=True)
        st.markdown(center_text(municipality_data["Turmas"]), unsafe_allow_html=True)
        #st.divider()


    with col4:
        st.markdown(center_and_bold_text("Teachers"), unsafe_allow_html=True)
        st.markdown(center_text(municipality_data["Docentes"]), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        #st.divider()


        st.markdown(center_and_bold_text("Student Techer Ratio"), unsafe_allow_html=True)
        st.markdown(center_text(student_teacher_ratio), unsafe_allow_html=True)
        #st.divider()

    #st.divider()

else:
    print("municipality_data Not Available..")

st.markdown("<br>", unsafe_allow_html=True)

if not funding_data.empty:

     # Color mapping for 'Status'
    color_mapping = {
#        'Actual': 'rgb(240, 242, 246)',
        'Actual': 'darkgray',
        'Predicted': 'rgb(75,126,255)'
    }

    # Create a Plotly bar chart
    fig = px.bar(funding_data, x='Year', y='Funding (R$)', color='Status',
                labels={'Funding (R$)': 'Funding in Million (R$)', 'Year': 'Year'},
                title='Yearly Funding',
                text='Funding (R$)',
                color_discrete_map=color_mapping)  # Custom color mapping

    # Customize the layout
    fig.update_layout(
        title_x=0.02,  # Center-align the title
        legend_title="",
        legend_orientation="h",  # horizontal orientation
        legend_x=0.8,  # x-position (center)
        legend_y=-0.1,  # y-position (bottom)
        yaxis=dict(showgrid=True),  # Remove horizontal gridlines
        #height=450  # Set the height of the chart


    )
    # Display the Plotly chart using Streamlit
    st.plotly_chart(fig, use_container_width=True)  # Set to full width
else:
    print("Funding Not Available..")
