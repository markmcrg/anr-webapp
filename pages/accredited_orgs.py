import streamlit as st
import pandas as pd
from st_keyup import st_keyup
import streamlit_antd_components as sac
# Add the main directory to the system path if necessary
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers import fetch_data
def accredited_orgs():
    
    
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
            org_data_df = org_data_df[org_data_df['Jurisdiction'] == selected_jurisdiction]
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
        org_query = None
        if not toggle_jurisdiction:
            org_query = st_keyup('Search for an organization:', debounce=300, key="0", placeholder="Organization Name/Abbreviation")
        if org_query:
            filtered_df = filtered_df[filtered_df['Organization Name'].str.contains(org_query, case=False, regex=False)]
        # Check if there are any results
        if filtered_df.empty:
            sac.result(label='No Results Found', description="We couldn't locate any matching results. Consider using different filters or keywords.", status='empty')
        else:

            
            org_table_data = """ 
                <tr>
                    <th class="text-center">SOCN</th>
                    <th class="text-center">Organization Name</th>
                    <th class="text-center">Jurisdiction</th>
                    <th class="text-center">Status</th>
                </tr>
            
            """
            for index, row in filtered_df.iterrows():
                # Create the <td> string for each column in the row
                # convert each value to string
                # remove newline in status column
                row['Status'] = row['Status'].replace('\n', ' ')
                org_table_data += f"""
                <tr>
                    <td class="socn-column">{row['SOCN']}</td>
                    <td>{row['Organization Name']}</td>
                    <td class="text-center">{row['Jurisdiction']}</td>
                    <td class="text-center">{row['Status']}</td>
                </tr>
                """
                
            html_code = f"""
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                <style>
                    h1 {{
                        font-family: "Source Sans Pro", sans-serif;
                        font-weight: 700;
                        color: rgb(49, 51, 63);
                        padding: 1.25rem 0px 1rem;
                        margin: 0px;
                        line-height: 1.2;
                    }}
                    .table {{
                        background-color: white;
                        border-radius: 15px;
                        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                        overflow: hidden;
                        margin-bottom: 0;
                        table-layout: auto;
                    }}
                    .table th {{
                        background-color: #800000;
                        color: white !important;
                        vertical-align: middle;
                    }}
                    .socn-column {{
                        white-space: nowrap;
                    }}
                    .table td {{
                        vertical-align: middle;
                    }}
                    .table ul {{
                        margin-bottom: -5px;
                    }}
                    .table-striped tbody tr:nth-of-type(odd) {{
                        background-color: rgba(128, 0, 0, 0.05);
                    }}
                    .text-center {{
                        text-align: center;
                    }}
                    
                    .table tbody tr:last-child td {{
                        border-bottom: none;
                    }}
                </style>
                
                <table class="table table-striped">
                    {org_table_data}
                </table>
            """
            st.markdown(html_code, unsafe_allow_html=True)
            
            # Back to top
            st.markdown("<a href='#list-of-accredited-organizations-for-term-2324'>Back to top</a>", unsafe_allow_html=True)