import streamlit as st
import streamlit_antd_components as sac
import streamlit_authenticator as stauth
from helpers import fetch_data, user_data_helper
import pandas as pd
import pages as pg

st.set_page_config(page_title="PUP SC COSOA AnR Portal", page_icon="🏫", layout="wide")
st.logo('logo.png')

with st.sidebar:
    menu_item = sac.menu([
        sac.MenuItem('Home', icon='house-fill', ),
        sac.MenuItem('Accredited Organizations', icon='card-list'),
        sac.MenuItem('Application Requirements', icon='file-earmark-text-fill'),
        sac.MenuItem('Frequently Asked Questions', icon='question-circle-fill'),
        sac.MenuItem('Sign Up', icon='door-open-fill'),
        sac.MenuItem('Login', icon='door-closed-fill'),

    ], open_all=False, return_index=True)
# I can set active page via index parameter in here using session state
st.write(menu_item)
if menu_item == 1:
    pg.accredited_orgs()
elif menu_item == 2:
    pg.application_requirements()
elif menu_item == 3:
    pg.faqs()

# Two options:
# render menus for each page
# or make a SPA with a single page and render the content of each page based on the menu item clicked
st.write('hi')
st.write(st.session_state)


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