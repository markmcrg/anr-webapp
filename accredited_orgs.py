import streamlit as st
import pandas as pd
from helpers import fetch_data

st.set_page_config(page_title="Accredited Organizations", page_icon="ℹ️", layout="wide")

st.logo('logo.png')

org_data = fetch_data('https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/accredited_orgs')

org_data = org_data['data']

columns = [col['col'] for col in org_data['columns']]
column_names = ["SOCN", "Organization Name", "Jurisdiction", "Status"]

org_data_df = pd.DataFrame(org_data['rows'], columns=columns)
org_data_df.columns = column_names
st.markdown("<h1 style='text-align: center;'>List of Accredited Organizations for Term 2324</h1>", unsafe_allow_html=True)
col1, col2 = st.columns([1.5, 8.5])

with col1:
    toggle_type = st.checkbox("Filter by type")
    if toggle_type:
        selected_type = st.radio("Select a type", ["Accredited", "Revalidated"], key="type")
    toggle_jurisdiction = st.checkbox("Filter by jurisdiction")

    # Filtering based on user inputs
    if toggle_jurisdiction:
        selected_jurisdiction = st.radio("Select a jurisdiction", org_data_df['Jurisdiction'].unique())
    else:
        selected_jurisdiction = None

    # Apply filtering
    if toggle_type:
        if selected_type == "Accredited":
            if toggle_jurisdiction and selected_jurisdiction:
                filtered_df = org_data_df[(org_data_df['Status'] == "Accredited") & (org_data_df['Jurisdiction'] == selected_jurisdiction)]
            else:
                filtered_df = org_data_df[org_data_df['Status'] == "Accredited"]
        elif selected_type == "Revalidated":
                if toggle_jurisdiction and selected_jurisdiction:
                    filtered_df = org_data_df[(org_data_df['Status'].str.contains("Revalidated")) & (org_data_df['Jurisdiction'] == selected_jurisdiction)]
                else:
                    filtered_df = org_data_df[org_data_df['Status'].str.contains("Revalidated")]

    else:
        filtered_df = org_data_df
with col2:
    filtered_df = filtered_df.style.hide(axis="index").set_table_styles([{
        'selector': '.col2, .col3',  
        'props': [
            ('text-align', 'center')
        ]
    }])
    st.markdown(f"<div style='max-width: fit-content; margin-inline: auto;'>{filtered_df.to_html(index=False)}</div>", unsafe_allow_html=True)
    st.markdown("<a href='#list-of-accredited-organizations-for-term-2324'>Back to top</a>", unsafe_allow_html=True)
