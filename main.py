import streamlit as st
import streamlit_antd_components as sac
import streamlit_authenticator as stauth
import pandas as pd
import pages as pg
from helpers import fetch_data, unpack_credentials

# Entrypoint / page router for the app

st.set_page_config(page_title="PUP SC COSOA AnR Portal", page_icon="🏫", layout="wide")
st.logo('logo.png')

with st.sidebar:
    if st.session_state["authentication_status"] == None or st.session_state["authentication_status"] == False:
        menu_item = sac.menu([
            sac.MenuItem('Home', icon='house-fill', ),
            sac.MenuItem('Accredited Organizations', icon='card-list'),
            sac.MenuItem('Application Requirements', icon='file-earmark-text-fill'),
            sac.MenuItem('Frequently Asked Questions', icon='question-circle-fill'),
            sac.MenuItem('Sign Up', icon='door-open-fill'),
            sac.MenuItem('Login', icon='door-closed-fill'),

        ], open_all=False, return_index=True)
    
    if st.session_state["authentication_status"]:
        menu_item = sac.menu([
            sac.MenuItem('Home', icon='house-fill', ),
            sac.MenuItem('Accredited Organizations', icon='card-list'),
            sac.MenuItem('Application Requirements', icon='file-earmark-text-fill'),
            sac.MenuItem('Frequently Asked Questions', icon='question-circle-fill'),
            sac.MenuItem('Sign Up', icon='door-open-fill'),
            sac.MenuItem('Logout', icon='door-closed-fill'),

        ], open_all=False, return_index=True)


if menu_item == 0:
    pg.home()
if menu_item == 1:
    pg.accredited_orgs()
elif menu_item == 2:
    pg.application_requirements()
elif menu_item == 3:
    pg.faqs()
elif menu_item == 4:
    pg.signup()
elif menu_item == 5:
    pg.login()

# Sidebar Footer Login info

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

if st.session_state["authentication_status"]:
    st.sidebar.write(f'*{st.session_state["name"]}*')
elif st.session_state["authentication_status"] is None or st.session_state["authentication_status"] == False:
    st.sidebar.write("No login")

