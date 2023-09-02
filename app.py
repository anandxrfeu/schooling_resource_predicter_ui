import pandas as pd
import numpy as np

import streamlit as st

# Define the years and the number of years
start_year = 2012
end_year = 2025
years = np.arange(start_year, end_year + 1)

# Define the start and end funding values
start_funding = 2090301
end_funding = 14000562

# Calculate the number of data points
num_points = len(years)

# Generate gradually increasing funding values using np.linspace
funding_values = np.linspace(start_funding, end_funding, num_points).astype(int)

# Create the DataFrame
fake_funding = pd.DataFrame({
    'Year': years,
    'Funding (R$)': funding_values
})



########################################################################
# UI
########################################################################

########################### Sidebar
municipality = st.sidebar.selectbox("**Choose a municipality**", ("Cerejeiras - Rondônia", "Terezinha - Bahia", "Prata - Minas Gerais"))

st.sidebar.markdown(
    "Predict education funding needs at a municipality level in Brazil. The underlyding model uses highschool data. "

)

st.sidebar.markdown(
    """
**Prediction parameters:**
"""
)

year = st.sidebar.slider(
    "Year", min_value=2022, max_value=2025, value=2023, step=1
)
passing_grade = st.sidebar.slider(
    "Passing %", min_value=80, max_value=99, value=85, step=5
)

st.sidebar.markdown(
    f"""
**Other parameters (circa 2020):**

    - Student falling rate 16%
    - Student dropour rate 2%
    - Number of schools 234
    - Number of teahers 2344
    - Population 2340944
    - GDP per capita R$ 17,234
    - Internet access 75.83%
"""
)

########################### Main panel

st.title(f"Funding Needs for {municipality.replace(' -', ',')}")

st.bar_chart(fake_funding, x="Year")
