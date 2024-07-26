import streamlit as st
from helpers import fetch_data, unpack_credentials
import streamlit_authenticator as stauth

# Insert login here so that it doesn't render in other pages

def login():
    st.write('login page')
    
    user_data = fetch_data('https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/users')['data']

    credentials = unpack_credentials(user_data)
    
    authenticator = stauth.Authenticate(credentials=credentials,
                                        cookie_name='pupsc-cosoa-anr-portal', 
                                        cookie_key='pupsc-cosoa-anr-portal-key', 
                                        cookie_expiry_days=30)


    authenticator.login()
    
    if st.session_state['authentication_status']:
        authenticator.logout()
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
