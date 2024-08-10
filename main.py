import streamlit as st
import streamlit_antd_components as sac
import streamlit_authenticator as stauth
import pandas as pd
import pages as pg
import time
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from helpers import fetch_data, get_email, unpack_credentials, get_role, get_abbreviation, update_last_login, modify_user_data
import mysql.connector
from mysql.connector import Error

# Entrypoint / page router for the app

st.set_page_config(page_title="PUP SC COSOA AnR Portal", page_icon="🏫", layout="wide")
st.logo('https://i.imgur.com/pA9lYh5.png', link='http://localhost:8501/') # Change link to sccosoa.com in production

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
            sac.MenuItem('Login', icon='bi bi-box-arrow-in-right'),
        ], open_all=False, index=2)
    
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
                sac.MenuItem('Account Settings', icon='bi bi-person-gear'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-in-left'),
            ], open_all=False, index=2)
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
                sac.MenuItem('Account Settings', icon='bi bi-person-gear'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-in-left'),
            ], open_all=False, index=2)
        elif role == 'chair':
            menu_item = sac.menu([
                sac.MenuItem(f'Welcome, Chair!', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Home', icon='bi bi-house-door'),
                sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
                sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
                sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),
                sac.MenuItem('View Submissions', icon='bi bi-clipboard-check'),
                sac.MenuItem('Account Settings', icon='bi bi-person-gear'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-in-left'),
                
                sac.MenuItem("", disabled=True),
                
                sac.MenuItem(f'Admin Tools', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Assign Organizations', icon='bi bi-person-check'),
                sac.MenuItem("User Management", icon='bi bi-person-lines-fill'),
                sac.MenuItem("Metrics", icon='bi bi-graph-up-arrow'),
            ], open_all=False, index=2)
        elif role == 'execcomm':
            menu_item = sac.menu([
                sac.MenuItem(f'Welcome, Executive Committee!', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Home', icon='bi bi-house-door'),
                sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
                sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
                sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),

                sac.MenuItem('Account Settings', icon='bi bi-person-gear'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-in-left'),
                
                sac.MenuItem("", disabled=True),

                sac.MenuItem('Admin Tools', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Assign Organizations', icon='bi bi-person-check'),
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
    with st.spinner("Loading..."):
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
elif menu_item == 'User Management':
    pg.user_management()

# Sidebar Footer Login info

if st.session_state["authentication_status"]:
    menu_item = 'Home'
elif st.session_state["authentication_status"] is None or st.session_state["authentication_status"] == False:
    pass

col1, col2 = st.columns([2,1])
if st.session_state["authentication_status"]:
    
    cols = st.columns([0.3, 1, 0.3], vertical_alignment='center')   

    with cols[1]:
        current_tab = sac.tabs([
        sac.TabsItem(label='Update Profile', icon='pencil-square'),
        sac.TabsItem(label='Update Email Address', icon='envelope'),
        sac.TabsItem(label='Update Password', icon='person-lock'),
    ], align='center', position='top', size='sm', variant='outline')
        if current_tab == 'Update Profile':
            with st.container(border=True):
                if 'abbreviation' not in st.session_state:
                    st.session_state['abbreviation'] = get_abbreviation(st.session_state["username"])
                if 'email' not in st.session_state:
                    st.session_state['email'] = get_email(st.session_state["username"])
                st.subheader('Account Information')
                org_name = st.text_input('**Organization Name**', value=st.session_state['name'])
                cols = st.columns(2)
                username = cols[1].text_input('**Username**', value=st.session_state["username"], disabled=True, help='Username cannot be changed.')
                abbreviation = cols[0].text_input('**Abbreviation**', value=get_abbreviation(st.session_state["username"]))
                email = st.text_input('**Email**', value=get_email(st.session_state["username"]), disabled=True, help='Email can be changed at the "Update Email Address" tab.')

                fields_blank = (
                    not org_name or org_name.strip() == '' or
                    not abbreviation or abbreviation.strip() == ''
                )
                
                # Dictionary to track changed fields and their new values
                changed_fields = {}

                # Check if each field has changed and update the dictionary
                if org_name != st.session_state['name']:
                    changed_fields['Organization Name'] = org_name
                if abbreviation != st.session_state['abbreviation']:
                    changed_fields['Abbreviation'] = abbreviation
                
                fields_changed = bool(changed_fields)
                
                update_records = st.button('Save', disabled=fields_blank or not fields_changed)
                if update_records:
                    updated_fields = []
                    msg = st.toast('Updating Records...', icon='🔄')
                    for field, new_value in changed_fields.items():
                        # Run the modify_user_data function for each changed field
                        affected_rows = modify_user_data("username", field, st.session_state["username"], new_value)
                    time.sleep(1)
                    msg.toast('Records Updated!', icon='✅')
                    time.sleep(1)
                    if updated_fields:
                        if len(updated_fields) == 1:
                            success_message = f"{updated_fields[0]} has been changed."
                        elif len(updated_fields) == 2:
                            success_message = f"{' and '.join(updated_fields)} have been changed."
                        else:
                            success_message = f"{', '.join(updated_fields[:-1])}, and {updated_fields[-1]} have been changed."

                        st.success(success_message)
                    sac.alert(label='Organization Name successfully changed.', description=success_message, size='sm', radius='lg', variant='quote-light', color='success', icon=True, closable=True)


        elif current_tab == 'Update Email Address':
            with st.container(border=True):
                st.subheader('Update Email Address')
                email = st.text_input('**Current Email**', value=get_email(st.session_state["username"]))
                new_email = st.text_input('**New Email**')
                st.button('Save', disabled=True)
        elif current_tab == 'Update Password':
            with st.container(border=True):
                st.subheader('Update Password')
                password = st.text_input('**Old Password**', type='password')
                new_password = st.text_input('**New Password**', type='password')
                confirm_password = st.text_input('**Confirm Password**', type='password')
                st.button('Save', disabled=True)
        

# add results screen

# can modify: org name, abbreviation password
# still show other fields but disable

# user - for orgs
# cosoa - for evals
# execcomm - for org assignment
# chair - for admin level access (see all user info and change access