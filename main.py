import streamlit as st
import streamlit_antd_components as sac
import pages as pg
from helpers import authenticate_b2, get_role, get_abbreviation, update_last_login, upload_document, list_files


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
        ], open_all=False, index=2)
    
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

# Sidebar Footer Login info

if st.session_state["authentication_status"]:
    menu_item = 'Home'
elif st.session_state["authentication_status"] is None or not st.session_state["authentication_status"]:
    pass

if st.session_state["authentication_status"]:
    st.markdown("<h1 style='text-align: center;'>Accreditation Application</h1><br><br>", unsafe_allow_html=True)
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'step_1_disabled' not in st.session_state:
        st.session_state.step_1_disabled = True
    if 'step_2_disabled' not in st.session_state:
        st.session_state.step_2_disabled = True
    if 'step_3_disabled' not in st.session_state:
        st.session_state.step_3_disabled = True
    if 'step_4_disabled' not in st.session_state:
        st.session_state.step_4_disabled = True
    if 'step_5_disabled' not in st.session_state:
        st.session_state.step_5_disabled = True
    if 'org_abbrv' not in st.session_state:
        st.session_state.org_abbrv = None
    if 'org_doc' not in st.session_state:
        st.session_state.org_doc = None
    if 'jurisdiction' not in st.session_state:
        st.session_state.jurisdiction = None
        
    def next_step():
        st.session_state.current_step += 1
        st.rerun()

    def prev_prev():
        st.session_state.current_step -= 1
        st.rerun()
    page_cols = st.columns([0.5, 0.1, 1, 0.1], vertical_alignment='center')
    with page_cols[0]:
        st.session_state.current_step = sac.steps(
            items=[
                sac.StepsItem(title='Application Information', disabled=st.session_state.step_1_disabled),
                sac.StepsItem(title='Organization Info', disabled=st.session_state.step_2_disabled),
                sac.StepsItem(title='Upload Documents', disabled=st.session_state.step_3_disabled),
                sac.StepsItem(title='Confirm Application', disabled=st.session_state.step_4_disabled),
                sac.StepsItem(title='Application Submitted!', disabled=st.session_state.step_5_disabled, icon='check-circle-fill'),
            ], return_index=True, placement='horizontal', direction='vertical', index=st.session_state.current_step
        )
        
    with page_cols[1]:
        st.html(
            '''
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 2px solid rgba(49, 51, 63, 0.2);
                        height: 500px;
                        margin: auto;
                    }
                </style>
            '''
        )
    if st.session_state.current_step == 0:
        with page_cols[2]:
            st.session_state.current_step = 0
            st.session_state.step_1_disabled = False
            st.write("")
            st.markdown("<h4 style='text-align: center;'>1. Select your application type, and the order of your application.</h1><br><br>", unsafe_allow_html=True)
            st.write("")
            cols = st.columns([0.2, 1,1, 0.2], gap='small', vertical_alignment='center')
            
            with cols[1]:
                with st.container(border=True):
                    st.session_state.app_type = sac.buttons([
                        sac.ButtonsItem(label='Accreditation', icon='check2-circle'),
                        sac.ButtonsItem(label='Revalidation', icon='arrow-repeat'),
                    ], label='', direction='vertical', gap='md', variant='outline', use_container_width=True, align='center', size='md', index=2)
            with cols[2]:
                with st.container(border=True):
                    st.session_state.app_order = sac.buttons([
                        sac.ButtonsItem(label='Initial Submission', icon='1-circle'),
                        sac.ButtonsItem(label='1st Resubmission', icon='2-circle'),
                        sac.ButtonsItem(label='2nd Resubmission', icon='3-circle'),
                    ], label='', direction='vertical', gap='md', variant='outline', use_container_width=True, align='center', size='md', index=3)
            next_btn = st.button("Next", key="next", disabled= not (st.session_state.app_type and st.session_state.app_order))
            if next_btn:
                next_step()
    if st.session_state.current_step == 1:
        st.session_state.current_step = 1
        st.session_state.step_2_disabled = False
        with page_cols[2]:
            st.header("2. Organization Info")
            abbreviation = get_abbreviation(st.session_state['username'])
            st.session_state.org_abbrv = f'{st.session_state["name"]} ({abbreviation})'
            st.text_input("**Complete Name of Student Organization (Abbreviation/Initialism)**", placeholder="PowerPuff Girls Ensemble (PPGE)", 
                                     value=st.session_state.org_abbrv, 
                                     disabled=True, 
                                     help='To modify this, please change your details in Account Settings.')
            st.session_state.jurisdiction = st.selectbox("**Jurisdiction**", 
                                        ["University-Wide (U-Wide)", "College of Architecture, Design, and the Built Environment (CADBE)", "College of Accountancy and Finance (CAF)", "College of Arts and Letters (CAL)", "College of Business Administration (CBA)", "College of Computer and Information Sciences (CCIS)", "College of Engineering (CE)", "College of Human Kinetics (CHK)", "College of Communication (COC)", "College of Education (COED)", "College of Political Science and Public Administration (CPSPA)", "College of Science (CS)", "College of Social Sciences and Development (CSSD)", "College of Tourism, Hospitality, and Transportation Management (CTHTM)", "Insititute of Technology (ITech)", "Open University System (OUS)", "Graduate School (GS)", "Lab High School (LHS)", "Senior High School (SHS)"], 
                                        help='This is where your organization and its members will be based.')
            next_btn = st.button("Next", key="next2")
            if next_btn:
                next_step()
    if st.session_state.current_step == 2:
        st.session_state.current_step = 2
        st.session_state.step_3_disabled = False
        with page_cols[2]:
            st.header("3. Upload Document Compilation")
            st.session_state.org_doc = st.file_uploader("Upload your document compilation here:", type=['pdf'], help='Please upload your document compilation in PDF format.', label_visibility='visible')
            next_btn = st.button("Next", key="next3", disabled= not st.session_state.org_doc)
        
            if st.session_state.org_doc is not None:
                sac.alert(label='File uploaded successfully.', size='sm', variant='quote-light', color='success', icon=True)
                
            if next_btn:
                next_step()
                
    if st.session_state.current_step == 3:
        st.session_state.current_step = 3
        st.session_state.step_4_disabled = False
        with page_cols[2]:
            st.header("4. Confirm Application")
            st.write(f"**Organization:** {st.session_state.org_abbrv}")
            st.write(f"**Jurisdiction:** {st.session_state.jurisdiction}")
            st.write(f"**Application Type:** {st.session_state.app_type}")
            st.write(f"**Application Order:** {st.session_state.app_order}")
            st.write(f"**Document Compilation:** {st.session_state.org_doc}")
        
            submit_btn = st.button("Submit Application", key="submit")
            if submit_btn:
                from helpers import authenticate_b2, get_download_url, upload_document, list_files
                msg = st.toast('Submitting Application...', icon='⬆️')
                bucket = authenticate_b2('anr-webapp')
                filename = f'{st.session_state.org_abbrv} - {st.session_state.app_order}'
                file_ver = upload_document(bucket, st.session_state.org_doc, filename)
                if file_ver:
                    msg.toast('Application submitted successfully!', icon='🎉')
                    next_step()
                
    if st.session_state.current_step == 4:
        st.session_state.current_step = 4
        for i in range(1, 6):
            st.session_state[f'step_{i}_disabled'] = True
        with page_cols[2]:
            sac.result(label='Application Submitted!', description='Please check the status of your submission by clicking on "Accreditation Status."', status='success')
        



        from helpers import authenticate_b2, get_download_url, upload_document, list_files

        bucket = authenticate_b2('anr-webapp')
        filename = f'{st.session_state.org_abbrv} - {st.session_state.app_order}' +'.pdf'
        list_files(bucket)
        pdf_url = get_download_url(bucket, filename)
        st.write(pdf_url)
    st.write(st.session_state)

# Upload file with filename of abbrv + app_type 
# Get link of doc from server 
# Insert link to submissions table with view (download link + auth token)
# Table headers: Organization Name + Abbreviation, app_type, app_order, username, jurisdiction, date submitted, eval_phase, assigned_to
# Disable certain app type once submitted by adding more headers to users table



# Display summary screen to review application details - once they submit, show warning that they can't edit anymore
# set up session state for variables for each step
# set up proper enabling of steps once visited
            
# user - for orgs
# cosoa - for evals
# execcomm - for org assignment
# chair - for admin level access (see all user info and change access