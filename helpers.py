import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

# Function to fetch data from the TiDB Cloud API
def fetch_data(url: str) -> dict:
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))
    return response.json()