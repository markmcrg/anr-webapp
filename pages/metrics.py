import streamlit as st
import streamlit_shadcn_ui as ui

# Add the main directory to the system path if necessary
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers import get_submission_count, get_user_count

def metrics():
    org_count = get_user_count('user')
    
    cosoa_count = get_user_count('cosoa')
    enbanc_count = get_user_count('enbanc')

    
    sub_count = get_submission_count()
    total_cosoa = int(cosoa_count) + int(enbanc_count)
    cols = st.columns([0.25, 1, 0.25])
    with cols[1]:
        with st.container(border=True):
            st.header("📊 Site Metrics")
            cols = st.columns(3)
            with cols[0]:
                ui.metric_card(title="Submissions", content=f"{sub_count}", key="card1")
            with cols[1]:
                ui.metric_card(title="User Accounts", content=f"{org_count}",  key="card2")
            with cols[2]:
                ui.metric_card(title="COSOA Accounts", content=f"{total_cosoa}", key="card3")