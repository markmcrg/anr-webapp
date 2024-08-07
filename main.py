from pyparsing import col
import streamlit as st
import streamlit_antd_components as sac
import streamlit_authenticator as stauth
import pandas as pd
import pages as pg
import time
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from helpers import fetch_data, unpack_credentials, get_role, get_abbreviation, update_last_login

# Entrypoint / page router for the app

st.set_page_config(page_title="PUP SC COSOA AnR Portal", page_icon="🏫", layout="wide")
st.logo('https://i.imgur.com/pA9lYh5.png')

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'name' not in st.session_state:
    st.session_state['name'] = None
    
    
with st.sidebar:
    if st.session_state["authentication_status"] == None or st.session_state["authentication_status"] == False:
        menu_item = sac.menu([
            sac.MenuItem('Guest Menu', disabled=True),
            sac.MenuItem(type='divider'),
            sac.MenuItem('Home', icon='bi bi-house-door'),
            sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
            sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
            sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),
            sac.MenuItem('Sign Up', icon='bi bi-person-plus'),
            sac.MenuItem('Login', icon='bi bi-box-arrow-right'),
        ], open_all=False)
    
    if st.session_state["authentication_status"]:
        role = get_role(st.session_state["username"])
        if role == 'cosoa':
            menu_item = sac.menu([
                sac.MenuItem(f'Welcome, Admin!', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Home', icon='bi bi-house-door'),
                sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
                sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
                sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),
                sac.MenuItem('View Submissions', icon='bi bi-file-earmark-text'),
                sac.MenuItem('Internal Evaluations', icon='bi bi-clipboard-check'),
                sac.MenuItem('Account Settings', icon='bi bi-person-plus'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-right'),
            ], open_all=False)
        elif role == 'user':
            abbreviation = get_abbreviation(st.session_state["username"])
            menu_item = sac.menu([
                sac.MenuItem(f'Welcome, {str(abbreviation)}!', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Home', icon='bi bi-house-door'),
                sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
                sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
                sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),
                sac.MenuItem('Accreditation Application', icon='bi bi-file-earmark-text'),
                sac.MenuItem('Accreditation Status', icon='bi bi-graph-up-arrow'),
                sac.MenuItem('Account Settings', icon='bi bi-person-plus'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-right'),
            ], open_all=False)
        elif role == 'chair':
            menu_item = sac.menu([
                sac.MenuItem(f'Welcome, Chair!', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Home', icon='bi bi-house-door'),
                sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
                sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
                sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),
                sac.MenuItem('Internal Evaluations', icon='bi bi-clipboard-check'),
                sac.MenuItem('Account Settings', icon='bi bi-person-plus'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-right'),
                
                sac.MenuItem("", disabled=True),
                
                sac.MenuItem(f'Admin Tools', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem("User Management", icon='bi bi-person-lines-fill'),
                sac.MenuItem("Metrics", icon='bi bi-graph-up-arrow'),
            ], open_all=False)
        elif role == 'execcomm':
            menu_item = sac.menu([
                sac.MenuItem(f'Welcome, Executive Committee!', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Home', icon='bi bi-house-door'),
                sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
                sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
                sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),
                sac.MenuItem('Admin Tools', icon='bi bi-clipboard-check'),
                sac.MenuItem('Account Settings', icon='bi bi-person-plus'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-right'),
            ], open_all=False)
        

if menu_item == 'Home':
    pg.home()
if menu_item == 'Accredited Organizations':
    pg.accredited_orgs()
elif menu_item == 'Application Requirements':
    pg.application_requirements()
elif menu_item == 'Frequently Asked Questions':
    pg.faqs()
elif menu_item == 'Sign Up':
    pg.signup()
elif menu_item == 'Login':
    pg.login()
    if st.session_state["authentication_status"]:
        menu_item = 'Home'
        update_last_login(st.session_state["username"])
        st.rerun()
elif menu_item == 'Logout':
    pg.login(logout=True)
elif menu_item == 'Accreditation Application':
    pg.accreditation_application()
elif menu_item == 'Accreditation Status':
    pg.accreditation_status()

# Sidebar Footer Login info

if st.session_state["authentication_status"]:
    menu_item = 'Home'
elif st.session_state["authentication_status"] is None or st.session_state["authentication_status"] == False:
    pass

users = fetch_data('https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_user_data')

user_data_columns = [col['col'] for col in users['data']['columns']]

columns_to_show = sac.checkbox(
    items=user_data_columns,
    label='User Data Columns', description='Click on the checkbox to toggle which columns to show', index=[1,2,3,4], align='start', size='sm', check_all='Select all', 
)

if columns_to_show:
    user_data = pd.DataFrame(users['data']['rows'], columns=columns_to_show)
    st.data_editor(user_data, key='user_data', hide_index=True)

    col1, col2 = st.columns(2)
    col3, col4, col5 = st.columns(3)
    with col2:
        with st.form(key='modify_email'):
            st.markdown("##### Modify Email")
            if 'email' not in columns_to_show:
                st.selectbox('Old Email', options=[], disabled=True)
                new_email = st.text_input('New Email', key='new_email', disabled=True)
                submit_email = st.form_submit_button('Modify',disabled=True)
                st.info("Please enable the 'email' column to modify email.")
            else:
                old_email = st.selectbox('Old Email', user_data['email'].tolist(), key='old_email', placeholder='Select an email')
                new_email = st.text_input('New Email', key='new_email')
                submit_email = st.form_submit_button('Modify')
            if submit_email:
                st.toast("Email modified successfully", icon="📧")
    with col1:
        with st.form(key='modify_roles'):
            st.markdown("##### Modify Roles")
            if 'username' not in columns_to_show or 'role' not in columns_to_show:
                username = st.selectbox('Username', options=[], disabled=True)
                st.selectbox('Role', options=[], disabled=True)
                submit_role = st.form_submit_button('Modify',disabled=True)
                st.info("Please enable the 'username' and 'role' column to modify roles.")
            else:
                username = st.selectbox('Username', user_data['username'].tolist(), key='username', placeholder='Select a username')
                role = st.selectbox('Role', ['user', 'cosoa', 'execcomm', 'chair'], key='role')
                submit_role = st.form_submit_button('Modify')
            if submit_role:
                st.toast("Role modified successfully", icon="👤")
    with col3:
        with st.form(key='modify_username'):
            st.markdown("##### Modify Username")
            if 'username' not in columns_to_show:
                st.selectbox('Old Username', options=[], disabled=True)
                new_username = st.text_input('New Username', key='new_username', disabled=True)
                submit_username = st.form_submit_button('Modify',disabled=True)
                st.info("Please enable the 'username' column to modify username.")
            else:
                old_username = st.selectbox('Old Username', user_data['username'].tolist(), key='old_username', placeholder='Select a username')
                new_username = st.text_input('New Username', key='new_username')
                submit_username = st.form_submit_button('Modify')
            if submit_username:
                st.toast("Username modified successfully", icon="👤")
    with col4:
        with st.form(key='modify_org_name'):
            st.markdown("##### Modify Organization Name")
            if 'org_name' not in columns_to_show:
                st.selectbox('Old Organization Name', options=[], disabled=True)
                new_org_name = st.text_input('New Organization Name', key='new_org_name', disabled=True)
                submit_org_name = st.form_submit_button('Modify',disabled=True)
                st.info("Please enable the 'org_name' column to modify organization name.")
            else:
                old_org_name = st.selectbox('Old Organization Name', user_data['org_name'].tolist(), key='old_org_name', placeholder='Select an organization name')
                new_org_name = st.text_input('New Organization Name', key='new_org_name')
                submit_org_name = st.form_submit_button('Modify')
            if submit_org_name:
                st.toast("Organization name modified successfully", icon="🏫")
    with col5:
        with st.form(key='modify_abbreviation'):
            st.markdown("##### Modify Abbreviation")
            if 'abbreviation' not in columns_to_show:
                st.selectbox('Old Abbreviation', options=[], disabled=True)
                new_abbreviation = st.text_input('New Abbreviation', key='new_abbreviation', disabled=True)
                submit_abbreviation = st.form_submit_button('Modify',disabled=True)
                st.info("Please enable the 'abbreviation' column to modify abbreviation.")
            else:
                old_abbreviation = st.selectbox('Old Abbreviation', user_data['abbreviation'].tolist(), key='old_abbreviation', placeholder='Select an abbreviation')
                new_abbreviation = st.text_input('New Abbreviation', key='new_abbreviation')
                submit_abbreviation = st.form_submit_button('Modify')
            if submit_abbreviation:
                st.toast("Abbreviation modified successfully", icon="🏫")

# user - for orgs
# cosoa - for evals
# execcomm - for org assignment
# chair - for admin level access (see all user info and change access


# Add initialism to user database for greeting