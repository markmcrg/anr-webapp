import streamlit as st
import streamlit_antd_components as sac
import streamlit_authenticator as stauth
from helpers import fetch_data, user_data_helper, render_menu, page_router
import pandas as pd


st.set_page_config(page_title="PUP SC COSOA AnR Portal", page_icon="🏫", layout="wide")
st.logo('logo.png')

# Render the menu
page_index = 0
selected_item = render_menu(page_index, 'admin', 'false')
page_router(selected_item, page_index)


# Two options:
# render menus for each page
# or make a SPA with a single page and render the content of each page based on the menu item clicked



user_data = fetch_data('https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/users')['data']


user_data_info = user_data_helper(user_data)

# Unpacking the user_data_info tuple
emails = user_data_info[0]
passwords = user_data_info[1]
org_name = user_data_info[2]
created_at = user_data_info[3]
last_login = user_data_info[4]
role = user_data_info[5]
usernames = user_data_info[6]


# Transforming the lists into the required dictionary format
credentials = {
    'usernames': {}
}

for username, email, password, org_name in zip(usernames, emails, passwords, org_name):
    credentials['usernames'][username] = {
        'email': email,
        'failed_login_attempts': 0,
        'logged_in': False,
        'name': org_name,
        'password': password
    }

authenticator = stauth.Authenticate(credentials=credentials,
                                    cookie_name='pupsc-cosoa-anr-portal', 
                                    cookie_key='pupsc-cosoa-anr-portal-key', 
                                    cookie_expiry_days=30)


authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.sidebar.write(f'*{st.session_state["name"]}*')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
    


# Footer Login info

# add calendar