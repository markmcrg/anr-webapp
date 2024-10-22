import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
import time
from st_keyup import st_keyup
import streamlit_antd_components as sac
import os
from helpers import fetch_data, authenticate_b2, generate_download_auth_token

def assign_orgs():
    # bucket = authenticate_b2('anr-webapp')
    # auth_token = generate_download_auth_token(bucket)
    with st.form(key="assign_orgs_form", border=True):
        st.subheader("📄 Organization Submissions")
        submission_data = fetch_data("https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_all_submissions")['data']['rows']

        submission_data_df = pd.DataFrame(submission_data, columns=["org_name", "jurisdiction", "app_type", "app_order", "date_submitted", "eval_phase", "b2_file_url"])
        
        # submission_data_df['b2_file_url'] = submission_data_df['b2_file_url'] + auth_token
        
        submission_data_df.columns = ['Organization Name', 'Jurisdiction', 'Application Type', 'Application Order', 'Date Submitted', "Evaluation Phase", "View"]
        submission_data_df['Date Submitted'] = pd.to_datetime(submission_data_df['Date Submitted'])
        cols = st.columns([1,1], vertical_alignment='center')
        with cols[0]:
            submission_query = st_keyup('Search for an organization or user:', debounce=300, key="0", placeholder="Organization Name/Abbreviation or Person Assigned")
        with cols[1]:
            eval_phase_filter = sac.checkbox(
                items=[
                    'IE',
                    'FE',
                    'CA',
                    'Returned',
                    'Approved',
                    'Rejected'
                ],
                label='Filter by evaluation phase', index=[0, 1, 2, 3], align='center'
            )

        if submission_query:
            submission_data_df = submission_data_df[
                submission_data_df['Organization Name'].str.contains(submission_query, case=False, regex=False)
            ]
        if eval_phase_filter:
            submission_data_df = submission_data_df[
                submission_data_df['Evaluation Phase'].isin(eval_phase_filter)
            ]
            
        # Check if df is empty
        if not submission_data_df.empty:
            updated_submissions_df = st.data_editor(submission_data_df,
                        column_config={
                            "Organization Name" : st.column_config.TextColumn(
                                "Organization Name", 
                                disabled=True),
                            "Jurisdiction" : st.column_config.TextColumn(
                                "Jurisdiction", 
                                disabled=True),
                            "Application Type" : st.column_config.TextColumn(
                                "Application Type", 
                                disabled=True),
                            "Application Order" : st.column_config.TextColumn(
                                "Application Order", 
                                disabled=True),
                            "View" : st.column_config.LinkColumn(
                                "View",
                                display_text="View",
                                disabled=True),
                            "Date Submitted" : st.column_config.DateColumn(
                                "Date Submitted",
                                format="D MMM YYYY, h:mm a",
                                disabled=True),
                            "Evaluation Phase" : st.column_config.SelectboxColumn(
                                "Evaluation Phase",
                                required=True,
                                options=["IE", "FE", "CA", "Returned", "Approved", "Rejected"],
                                )
                        },
                        
                        hide_index=True) 
            if st.form_submit_button("Update"):
                try:
                    connection = mysql.connector.connect(
                        host=os.environ['db2_host'],
                        user=os.environ['db2_user'],
                        port=os.environ['db2_port'],
                        password=os.environ['db2_password'],
                        database=os.environ['db2_database'],
                    )
                except Error as e:
                    st.error(f"The error '{e}' occurred")
                    
                cursor = connection.cursor()
                
                for index, row in updated_submissions_df.iterrows():
                    evaluation_phase = row["Evaluation Phase"]
                    org_name = row["Organization Name"] 
                    app_order = row["Application Order"]  

                    # Construct the SQL UPDATE query
                    sql_query = """
                    UPDATE submissions
                    SET `eval_phase` = %s 
                    WHERE `org_name` = %s AND `app_order` = %s
                    """
                    cursor.execute(sql_query, (evaluation_phase, org_name, app_order))
                    
                try:
                    connection.commit()
                    cursor.close()
                    connection.close()
                    st.toast("Records updated successfully!", icon="✅")
                    time.sleep(2)
                except Error as e:
                    st.toast(f"The error '{e}' occurred", icon="❌")
                    cursor.close()
                    connection.close()
                st.rerun()
                
        else:
            sac.result(label='No Results Found', description="We couldn't locate any matching results.", status='empty')

if __name__ == "__main__":
    assign_orgs()