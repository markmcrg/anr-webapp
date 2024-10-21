import streamlit as st
from helpers import fetch_data, unpack_credentials
import streamlit_authenticator as stauth

import streamlit_antd_components as sac
import hydralit_components as hc
# Insert login here so that it doesn't render in other pages

def login(logout: bool = False):
    with st.container():
        user_data = fetch_data('https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/users')['data']

        credentials = unpack_credentials(user_data)
    
        authenticator = stauth.Authenticate(credentials=credentials,
                                            cookie_name='pupsc-cosoa-anr-portal', 
                                            cookie_key='pupsc-cosoa-anr-portal-key', 
                                            cookie_expiry_days=30)
        cols = st.columns([0.5, 1, 0.5])
        with cols[1]:
            authenticator.login()
        
        if st.session_state['authentication_status'] and logout:
            authenticator.logout(location='unrendered')
        if st.session_state["authentication_status"] is False:
            with cols[1]:
                st.error("Username or password is incorrect. Please try again.")

