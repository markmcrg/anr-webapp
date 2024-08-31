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

from helpers import fetch_data, submit_evaluation_accre, submit_evaluation_reval, modify_eval_phase
import pandas as pd
from st_keyup import st_keyup
import time
# add filters for which eval phase to show
submission_data = fetch_data("https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_all_submissions")['data']['rows']
submission_data_df = pd.DataFrame(submission_data)
submission_data_df = submission_data_df.rename(columns={"filename": "Organization Submission", "jurisdiction": "Jurisdiction", "app_type": "Application Type", "date_submitted": "Date Submitted", "eval_phase": "Evaluation Phase", "b2_file_url": "View"})

submission_data_df['Date Submitted'] = pd.to_datetime(submission_data_df['Date Submitted'])

top_cols = st.columns([2, 1, 1], vertical_alignment='center')
with top_cols[0]:
    submission_query = st_keyup('Search for an organization or user:', debounce=300, key="1", placeholder="Organization Name/Abbreviation or Person Assigned")
with top_cols[1]:
    eval_phase_filter = sac.checkbox(
        items=[
            'IE',
            'FE',
            'CA',
        ],
        label='Filter by evaluation phase', index=[0, 1, 2, 3], align='center'
    )
if submission_query:
    submission_data_df = submission_data_df[
        submission_data_df['Organization Submission'].str.contains(submission_query, case=False, regex=False)
    ]
if eval_phase_filter:
    submission_data_df = submission_data_df[
        submission_data_df['Evaluation Phase'].isin(eval_phase_filter)
    ]

st.dataframe(submission_data_df, hide_index=True, column_order=['Organization Submission', 'Jurisdiction', 'Application Type', 'Date Submitted', 'Evaluation Phase', 'View'])
cols = st.columns([1,1], gap="medium")
eval_data = {}
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
def display_previous_remarks(data, doc_code, idx):
    with st.popover("View Previous Remarks"):
        prev_remark = data[f'REQ{idx:03d}']['remarks']
        st.write('\n'.join(
            line if line.strip().startswith('- ') else f'- {line.strip()}'
            for line in prev_remark.split('\n') if line.strip()
        ))

def show_expander(documents, data=None):
    for idx, (doc_code, doc_name) in enumerate(documents.items(), start=1):
        with st.expander(f"{doc_code} - {doc_name}"):
            if data:
                display_previous_remarks(data, doc_code, idx)
            remark = st.text_area(f"Remarks for {doc_name}", key=f"remark_{doc_code}", height=100)
            approved = st.checkbox(f"Approve {doc_code}", key=f"approve_{doc_code}")
            eval_data[doc_code] = {"approved": approved, "remark": remark}

def get_filtered_record(submission_data_df, sub_to_eval, exclude_phase='IE'):
    return submission_data_df[
        (submission_data_df['Evaluation Phase'] != exclude_phase) &
        (submission_data_df['Organization Submission'] == sub_to_eval)
    ]

def extract_data(filtered_record, num_requirements):
    data = {}
    if not filtered_record.empty:
        for i in range(1, num_requirements + 1):
            req_key = f'REQ{i:03d}'
            data[req_key] = {
                'approved': filtered_record[f'{req_key}_approved'].values[0],
                'remarks': filtered_record[f'{req_key}_remarks'].values[0]
            }
    return data

if not submission_data_df.empty:
    with cols[0]:
        sub_to_eval = st.selectbox("**Select submission to evaluate:**", submission_data_df['Organization Submission'])
        
        eval_phase = submission_data_df[
            submission_data_df['Organization Submission'] == sub_to_eval
        ]['Evaluation Phase'].item()
        
        app_type = submission_data_df[
            submission_data_df['Organization Submission'] == sub_to_eval
        ]['Application Type'].item()
        
        with st.form("evaluation_form", border=False):
            if eval_phase == 'IE':
                if app_type == 'Accreditation':
                    show_expander(accre_docs)
                elif app_type == 'Revalidation':
                    show_expander(reval_docs)

            elif eval_phase in ['FE', 'CA']:
                filtered_record = get_filtered_record(submission_data_df, sub_to_eval)
                st.write(filtered_record)
                num_requirements = 6 if app_type == 'Accreditation' else 9
                data = extract_data(filtered_record, num_requirements)

                if app_type == 'Accreditation':
                    show_expander(accre_docs, data)
                elif app_type == 'Revalidation':
                    show_expander(reval_docs, data)

            save_btn = st.form_submit_button("Save")
        
        if 'show_eval_sumamary' not in st.session_state:
            st.session_state['show_eval_sumamary'] = False
            
        if save_btn:
            if any(not doc_data['remark'] for doc_data in eval_data.values()):
                sac.alert(label='Please provide remarks for all documents.', size='sm', variant='quote-light', color='info', icon=True)
            else:
                st.session_state['show_eval_sumamary'] = True
        if st.session_state['show_eval_sumamary']:
            with cols[1]:
                st.subheader("⭐ Evaluation Summary")
                eval_summary = pd.DataFrame(eval_data).T
                st.table(eval_summary)
                
                
                if eval_phase == "IE":
                    sac.alert(label='Once you click on confirm, your evaluation will be submitted and transferred to your final evaluator.', size='sm', variant='quote-light', color='info', icon=True)
                elif eval_phase == "FE":
                    new_status = sac.chip(
                        items=[
                            sac.ChipItem(label='Returned for Revisions', icon='bi bi-arrow-counterclockwise'),
                            sac.ChipItem(label='Chairperson\'s Approval', icon='bi bi-check-circle'),
                        ], label='Status', description='Once you click on confirm, your evaluation will be submitted and transferred to the next phase.', index=2, align='start', radius='md', variant='light',
                    )

                    
                confirm_btn = st.button("Confirm Evaluation", disabled=not new_status)
                if confirm_btn:
                    msg = st.toast("Submitting Evaluation...", icon="🔃")
                    # Save evaluation data to database
                    with st.spinner("Submitting Organization Evaluation..."):
                        if str(app_type) == "Accreditation":
                            response_code = submit_evaluation_accre(sub_to_eval, eval_data)
                        elif str(app_type) == "Revalidation":
                            response_code = submit_evaluation_reval(sub_to_eval, eval_data)
                        if response_code:
                            modify_eval_phase(sub_to_eval, eval_phase)
                            time.sleep(2)
                            msg.toast("Evaluation submitted successfully.", icon="✅")
                            st.session_state['show_eval_sumamary'] = False
                            sac.alert(label='Evaluation submitted successfully.', size='sm', variant='quote-light', color='success', icon=True)
                            
else:
    sac.result(label='No Results Found', description="We couldn't locate any matching submissions.", status='empty')
            
# implement changing of phases after submitting, show dropdown only if phase is FE or CA, if not, then just transfer to FE
# change the name 'view submissions' to 'evaluate submissions'
# Show tracker form for each submission on evaluator side Tracker form name, form code, status (approved/for revision)
# CA should only be visible to chair role
# Make new page for chair approve orgs ?
# Show org submissions returned for revisions


# user - for orgs
# cosoa - for evals
# execcomm - for org assignment
# chair - for admin level access (see all user info and change access