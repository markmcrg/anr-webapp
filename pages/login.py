import streamlit as st
from helpers import fetch_data
import streamlit_authenticator as stauth
import pandas as pd
import streamlit_antd_components as sac
import hydralit_components as hc
# Insert login here so that it doesn't render in other pages

def login(logout: bool = False):
    if not st.session_state['authentication_status'] and not logout: 
        cols = st.columns([0.5, 1, 0.5])
        with cols[1]:
            st.markdown("<h1 style='color: #f5c472; text-align:center;'>Login</h1>", unsafe_allow_html=True)
            with st.form("login_form"):
                username = st.text_input("**Username**", placeholder="pupsccosoa")
                password = st.text_input("**Password**", type="password")
                submitted = st.form_submit_button("Login", type="primary")
                
                if submitted:
                    user_data = fetch_data('https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/users')['data']
                    user_data_df = pd.DataFrame(
                        user_data["rows"], columns=[col["col"] for col in user_data["columns"]]
                    )
                    matching_user = user_data_df[(user_data_df['username'] == username) & (user_data_df['password'] == password)]
                    
                    if not matching_user.empty:
                        st.success("Login successful.")
                        org_name = matching_user['org_name'].values[0]
                        
                        # Set session state variables
                        st.session_state['authentication_status'] = True
                        st.session_state['username'] = username
                        st.session_state['name'] = org_name
                        
                        st.rerun()
                        
                    else:
                        st.error("Username or password is incorrect. Please try again.")
    
    if st.session_state['authentication_status'] and logout:
        st.session_state['authentication_status'] = None
        del st.session_state['username']
        del st.session_state['name']



