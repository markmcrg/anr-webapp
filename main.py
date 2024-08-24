import streamlit as st
import streamlit_antd_components as sac
import pages as pg
from helpers import get_role, get_abbreviation, update_last_login


# Entrypoint / page router for the app

st.set_page_config(page_title="PUP SC COSOA AnR Portal", page_icon="🏫", layout="wide")
st.logo('https://i.imgur.com/pA9lYh5.png', link='http://localhost:8501/') # Change link to sccosoa.com in production

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'name' not in st.session_state:
    st.session_state['name'] = None


with st.sidebar:
    if st.session_state["authentication_status"] is None or not st.session_state["authentication_status"] :
        menu_item = sac.menu([
            sac.MenuItem('Guest Menu', disabled=True),
            sac.MenuItem(type='divider'),
            sac.MenuItem('Home', icon='bi bi-house-door'),
            sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
            sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
            sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),
            sac.MenuItem('Sign Up', icon='bi bi-person-plus'),
            sac.MenuItem('Login', icon='bi bi-box-arrow-in-right'),
            sac.MenuItem('Password Reset', icon='bi bi-key'),
        ], open_all=False, index=2, size ='md')
    
    if st.session_state["authentication_status"]:
        role = get_role(st.session_state["username"])
        if role == 'cosoa':
            menu_item = sac.menu([
                sac.MenuItem('Welcome, Admin!', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Home', icon='bi bi-house-door'),
                sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
                sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
                sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),
                sac.MenuItem('View Submissions', icon='bi bi-file-earmark-text'),
                sac.MenuItem('Account Settings', icon='bi bi-person-gear'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-in-left'),
            ], open_all=False, index=2)
        elif role == 'user':
            abbreviation = get_abbreviation(st.session_state["username"])
            menu_item = sac.menu([
                sac.MenuItem(f'Welcome, {str(abbreviation)}!', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Home', icon='bi bi-house-door'),
                sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
                sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
                sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),
                sac.MenuItem('Accreditation Application', icon='bi bi-file-earmark-text'),
                sac.MenuItem('Accreditation Status', icon='bi bi-graph-up-arrow'),
                sac.MenuItem('Account Settings', icon='bi bi-person-gear'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-in-left'),
            ], open_all=False, index=2)
        elif role == 'chair':
            menu_item = sac.menu([
                sac.MenuItem('Welcome, Chair!', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Home', icon='bi bi-house-door'),
                sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
                sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
                sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),
                sac.MenuItem('View Submissions', icon='bi bi-clipboard-check'),
                sac.MenuItem('Account Settings', icon='bi bi-person-gear'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-in-left'),
                
                sac.MenuItem("", disabled=True),
                
                sac.MenuItem('Admin Tools', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Assign Organizations', icon='bi bi-person-check'),
                sac.MenuItem("User Management", icon='bi bi-person-lines-fill'),
                sac.MenuItem("Metrics", icon='bi bi-graph-up-arrow'),
            ], open_all=False, index=2)
        elif role == 'execcomm':
            menu_item = sac.menu([
                sac.MenuItem('Welcome, Executive Committee!', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Home', icon='bi bi-house-door'),
                sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
                sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
                sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),

                sac.MenuItem('Account Settings', icon='bi bi-person-gear'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-in-left'),
                
                sac.MenuItem("", disabled=True),

                sac.MenuItem('Admin Tools', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Assign Organizations', icon='bi bi-person-check'),
            ], open_all=False)
        
if menu_item == 'Home':
    pg.home()
if menu_item == 'Accredited Organizations':
    pg.accredited_orgs()
elif menu_item == 'Application Requirements':
    pg.application_requirements()
elif menu_item == 'Frequently Asked Questions':
    pg.faqs()
elif menu_item == 'Sign Up':
    pg.signup()
elif menu_item == 'Login':
    with st.spinner("Loading..."):
        pg.login()
        if st.session_state["authentication_status"]:
            menu_item = 'Home'
            update_last_login(st.session_state["username"])
            st.rerun()
elif menu_item == 'Logout':
    pg.login(logout=True)
elif menu_item == 'Accreditation Application':
    pg.accreditation_application()
elif menu_item == 'Accreditation Status':
    pg.accreditation_status()
elif menu_item == 'User Management':
    pg.user_management()
elif menu_item == 'Account Settings':
    pg.account_settings()
elif menu_item == 'Password Reset':
    pg.forgot_password()
elif menu_item == "Assign Organizations":
    pg.assign_orgs()
    
# Sidebar Footer Login info

if st.session_state["authentication_status"]:
    menu_item = 'Home'
elif st.session_state["authentication_status"] is None or not st.session_state["authentication_status"]:
    pass

from helpers import fetch_data
import pandas as pd
import mysql.connector
from mysql.connector import Error

if st.session_state["authentication_status"]:
    st.subheader("Organization Submissions")
    submission_data = fetch_data("https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_all_submissions")['data']['rows']
    cosoa_names = [d['org_name'] for d in fetch_data("https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_cosoa_users")['data']['rows']]

    submission_data_df = pd.DataFrame(submission_data, columns=["org_name", "jurisdiction", "app_type", "app_order", "date_submitted", "eval_phase", "assigned_to_username", "b2_file_url"])
    submission_data_df.columns = ['Organization Name', 'Jurisdiction', 'Application Type', 'Application Order', 'Date Submitted', "Evaluation Phase", "Person Assigned", "View"]
    submission_data_df['Date Submitted'] = pd.to_datetime(submission_data_df['Date Submitted'])
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
                    "Evaluation Phase" : st.column_config.SelectboxColumn(\
                        "Evaluation Phase",
                        required=True,
                        options=["IE1", "IE2", "FE1", "FE2"]
                        ),
                        "Person Assigned" : st.column_config.SelectboxColumn(\
                        "Person Assigned",
                        required=False,
                        options=cosoa_names,
                        width="medium"
                        )
                },
                
                hide_index=True) 
    if st.button("Update"):
        try:
            connection = mysql.connector.connect(
                host=st.secrets['anr_webapp_db2']['host'],
                user=st.secrets['anr_webapp_db2']['user'],
                port=st.secrets['anr_webapp_db2']['port'],
                password=st.secrets['anr_webapp_db2']['password'],
                database=st.secrets["anr_webapp_db2"]["database"],
            )
        except Error as e:
            st.error(f"The error '{e}' occurred")
        cursor = connection.cursor()
        for index, row in updated_submissions_df.iterrows():
            evaluation_phase = row["Evaluation Phase"]
            person_assigned = row["Person Assigned"]
            org_name = row["Organization Name"]  # Replace with your actual column name
            app_order = row["Application Order"]  # Replace with your actual column na

            # Construct the SQL UPDATE query
            sql_query = """
            UPDATE submissions
            SET `eval_phase` = %s, `assigned_to_username` = %s
            WHERE `org_name` = %s AND `app_order` = %s
            """
            cursor.execute(sql_query, (evaluation_phase, person_assigned, org_name, app_order))

            # return affected rows
            affected_rows = cursor.rowcount
    
        connection.commit()
        cursor.close()
        connection.close()
        st.rerun()

# assign orgs page has to have search bar, show unassigned orgs, show assigned orgs, show orgs assigned to user, add filters

# user - for orgs
# cosoa - for evals
# execcomm - for org assignment
# chair - for admin level access (see all user info and change access