import streamlit as st
import streamlit_antd_components as sac
import streamlit_shadcn_ui as ui
import pandas as pd
from helpers import fetch_data, unpack_credentials

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
        else:
            st.error("Username or password is incorrect. Please try again.")