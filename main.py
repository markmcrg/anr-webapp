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
                sac.MenuItem('View Submissions', icon='bi bi-clipboard-check'),
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
elif menu_item == "View Submissions":
    pg.view_submissions() 
# Sidebar Footer Login info

if st.session_state["authentication_status"]:
    menu_item = 'Home'
elif st.session_state["authentication_status"] is None or not st.session_state["authentication_status"]:
    pass

from helpers import fetch_data
import pandas as pd
# add filters for which eval phase to show
submission_data = fetch_data("https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_all_submissions")['data']['rows']
submission_data_df = pd.DataFrame(submission_data, columns=["filename", "jurisdiction", "app_type", "date_submitted", "eval_phase", "b2_file_url"])
submission_data_df.columns = ["Organization Submission", "Jurisdiction", "Application Type", "Date Submitted", "Evaluation Phase", "View"]
st.dataframe(submission_data_df, hide_index=True)
cols = st.columns([1,1], gap="medium")
approval_data = {}
accre_docs = {
    'AD001': 'Compilation of Compulsory Certificates',
    'AD002': 'Official List of Officers and Adviser(s)',
    'AD003': 'Officers’ Profile with 1st Semester COR',
    'AD004': 'Adviser(s)’s Letter of Concurrence',
    'AD005': 'Student Organization’s Constitution and Bylaws (CBL)',
    'AD006': 'General Plan of Activities with Budgetary Outlay',
}
reval_docs = {
    'RD001': 'Compilation of Compulsory Certificates',
    'RD002': 'Official List of Officers and Adviser(s)',
    'RD003': 'Officers’ Profile with 1st Semester COR',
    'RD004': 'Adviser(s)’s Letter of Concurrence',
    'RD005': 'Student Organization’s Constitution and Bylaws (CBL)',
    'RD006': 'General Plan of Activities with Budgetary Outlay',
    'RD007': 'Accomplishment Report',
    'RD008': 'Copy of Approved Financial Statements',
    'RD009': 'Turnover of Assets and Funds',
}

with cols[0]:
    sub_to_eval = st.selectbox("**Select submission to evaluate:**", submission_data_df['Organization Submission'])
    # Check app type of submission to know if ad or rd dict to use
    # Check app_order to know whether to show previous remarks (if FE), or not, then whether to show option to return with revised comments (if FE), or transfer to OC Endorsement
    if submission_data_df[submission_data_df['Organization Submission'] == sub_to_eval]['Application Type'].values[0] == 'Accreditation':
        for doc_code, doc_name in accre_docs.items():
            with st.expander(f"{doc_code} - {doc_name}"):
                remark = st.text_area(f"Remarks for {doc_name}", key=f"remark_{doc_code}", height=100)
                approved = st.checkbox(f"Approve {doc_code}", key=f"approve_{doc_code}")
                
                approval_data[doc_code] = {"approved": approved, "remark": remark}
                
    elif submission_data_df[submission_data_df['Organization Submission'] == sub_to_eval]['Application Type'].values[0] == 'Revalidation':
        for doc_code, doc_name in reval_docs.items():
            with st.expander(f"{doc_code} - {doc_name}"):
                remark = st.text_area(f"Remarks for {doc_name}", key=f"remark_{doc_code}", height=100)
                approved = st.checkbox(f"Approve {doc_code}", key=f"approve_{doc_code}")
                
                approval_data[doc_code] = {"approved": approved, "remark": remark}

    save_btn = st.button("Save")

if save_btn:
    if any([approval_data[doc]['remark'] == "" for doc in accre_docs]):
        with cols[0]:
            sac.alert(label='Please ensure that there are remarks for each document.', size='sm', variant='quote-light', color='warning', icon=True)
    else:
        with cols[1]:
            st.subheader("⭐ Evaluation Summary")
            # show st.table
            eval_summary = pd.DataFrame(approval_data).T
            st.table(eval_summary)
            
            confirm_btn = st.button("Confirm Evaluation")
            


# user - for orgs
# cosoa - for evals
# execcomm - for org assignment
# chair - for admin level access (see all user info and change access