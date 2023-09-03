import wikipedia
from streamlit_searchbox import st_searchbox
from typing import List, Optional

import streamlit as st
import os
import pandas as pd


folder_path = "/raw_data/"
file_name = "municipality_lookup.csv"
file_path = os.path.join(os.getcwd()+folder_path, file_name)
municipalities = pd.read_csv(file_path)

# Function to search for municipalities and return them in the specified format
def search_municipality(query: str, dataframe: pd.DataFrame) -> List[str]:
    # Case-insensitive search for the query in the 'Município' column
    filtered_df = dataframe[dataframe['Município'].str.contains(query, case=False)]

    # Create a list of string representation of "Município, Estado"
    results = [f"{row['Município']}, {row['Estado']}" for _, row in filtered_df.iterrows()]

    return results


# Function to lookup Código_IBGE based on "Município, Estado"
def lookup_codigo_ibge(municipio_estado: str, dataframe: pd.DataFrame) -> Optional[int]:
    # Split the input string into Municipio and Estado
    municipio, estado = municipio_estado.split(", ")

    # Filter the DataFrame to find the matching row
    filtered_df = dataframe[(dataframe['Município'] == municipio) & (dataframe['Estado'] == estado)]

    # If a match is found, return the Código_IBGE, otherwise return None
    if not filtered_df.empty:
        return int(filtered_df.iloc[0]['Código_IBGE'])
    else:
        return None


# function with list of labels
def search_wikipedia(searchterm: str) -> List[any]:
    return search_municipality(searchterm, municipalities) if searchterm else []

# pass search function to searchbox
selected_value = st_searchbox(
    search_wikipedia,
    key="municipality_searchbox",
    placeholder="Search for municipality..",
)

if selected_value:
    st.write(selected_value)
    ibge = lookup_codigo_ibge(selected_value, municipalities)
    st.write(ibge)
