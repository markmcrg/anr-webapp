import streamlit as st
import streamlit_shadcn_ui as ui
# Add the main directory to the system path if necessary
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers import fetch_data

def metrics():
    with st.container(border=True):
        st.header("📊 Site Metrics")
        users = fetch_data('https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_user_data')
        cols = st.columns(3)
        with cols[0]:
            ui.metric_card(title="Submission Count", content="$45,231.89", key="card1")
        with cols[1]:
            ui.metric_card(title="Organization Accounts", content="$45,231.89",  key="card2")
        with cols[2]:
            ui.metric_card(title="COSOA Accounts", content="$45,231.89", key="card3")
            
if __name__ == "__main__":
    metrics()