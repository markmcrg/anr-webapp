import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import streamlit_antd_components as sac

# Function to fetch data from the TiDB Cloud API
def fetch_data(url: str) -> dict:
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))
    return response.json()

def user_data_helper(user_data: dict) -> tuple:
    user_data_df = pd.DataFrame(user_data['rows'], columns=[col['col'] for col in user_data['columns']])
    email = user_data_df['email'].tolist()
    password = user_data_df['password'].tolist()
    org_name = user_data_df['org_name'].tolist()
    created_at = user_data_df['created_at'].tolist()
    last_login = user_data_df['last_login'].tolist()
    username = user_data_df['username'].tolist()
    role = user_data_df['role'].tolist()
    
    return email, password, org_name, created_at, last_login, role, username


# I can make a render menu helper function to render the menu for each page along with conditions on what to show depending on the user's role and login status
def render_menu(active_index, role, login_status):
    with st.sidebar:
        menu_item = sac.menu([
            sac.MenuItem('Home', icon='house-fill', ),
            sac.MenuItem('Accredited Organizations', icon='card-list'),
            sac.MenuItem('Application Requirements', icon='file-earmark-text-fill'),
            sac.MenuItem('Frequently Asked Questions', icon='question-circle-fill'),
            sac.MenuItem('Sign Up', icon='door-open-fill'),
            sac.MenuItem('Login', icon='door-closed-fill'),

        ], open_all=False, index=active_index, return_index=True)
        return menu_item
    
def page_router(active_index, current_index):
    if active_index != current_index:
        if active_index == 1:
            st.switch_page('pages/accredited_orgs.py')
        elif active_index == 0:
            st.switch_page('main.py')