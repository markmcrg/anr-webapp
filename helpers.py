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

def unpack_credentials(user_data: dict) -> dict:
    user_data_df = pd.DataFrame(user_data['rows'], columns=[col['col'] for col in user_data['columns']])
    emails = user_data_df['email'].tolist()
    passwords = user_data_df['password'].tolist()
    org_names = user_data_df['org_name'].tolist()
    created_at = user_data_df['created_at'].tolist()
    last_login = user_data_df['last_login'].tolist()
    usernames = user_data_df['username'].tolist()
    roles = user_data_df['role'].tolist()
    
    credentials = {
        'usernames': {}
    }
    for username, email, password, org_name in zip(usernames, emails, passwords, org_names):
        credentials['usernames'][username] = {
            'email': email,
            'failed_login_attempts': 0,
            'logged_in': False,
            'name': org_name,
            'password': password
        }

    return credentials


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

def register_user(abbreviation, email, org_name, password, role, username):
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key
    
    url = 'https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/users'
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    data = {
        "abbreviation": abbreviation,
        "email": email,
        "org_name": org_name,
        "password": password,
        "role": role,
        "username": username
    }
    
    response = requests.post(url, headers=headers, json=data, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))
    
    return response.status_code

def check_user(username):
    pass

def check_email(email):
    pass