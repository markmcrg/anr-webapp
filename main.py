import streamlit as st
import streamlit_antd_components as sac
import pages as pg
import time
from helpers import get_email, get_role, get_abbreviation, update_last_login, modify_user_data, get_name, send_otp_email
import random

# Entrypoint / page router for the app

st.set_page_config(page_title="PUP SC COSOA AnR Portal", page_icon="🏫", layout="wide")
st.logo('https://i.imgur.com/pA9lYh5.png', link='http://localhost:8501/') # Change link to sccosoa.com in production
if 'entered_otp' not in st.session_state:
    st.session_state.entered_otp = None
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'generated_otp' not in st.session_state:
    st.session_state.generated_otp = None
if 'verification_initiated' not in st.session_state:
    st.session_state.verification_initiated = False
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'name' not in st.session_state:
    st.session_state['name'] = None
if 'otp_attempts' not in st.session_state:
    st.session_state.otp_attempts = 0
if 'lockout_time' not in st.session_state:
    st.session_state.lockout_time = 60
def is_locked_out():
    if st.session_state.lockout_time and time.time() < st.session_state.lockout_time:
        return True
    return False    
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

# Sidebar Footer Login info

if st.session_state["authentication_status"]:
    menu_item = 'Home'
elif st.session_state["authentication_status"] is None or not st.session_state["authentication_status"]:
    pass

col1, col2 = st.columns([2,1])
if st.session_state["authentication_status"]:
    
    cols = st.columns([0.3, 1, 0.3], vertical_alignment='center')   

    with cols[1]:
        current_tab = sac.tabs([
        sac.TabsItem(label='Update Profile', icon='pencil-square'),
        sac.TabsItem(label='Update Email Address', icon='envelope'),
        sac.TabsItem(label='Update Password', icon='person-lock'),
    ], align='center', position='top', size='sm', variant='outline')
        if current_tab == 'Update Profile':
            with st.container(border=True):
                if 'abbreviation' not in st.session_state:
                    st.session_state['abbreviation'] = None
                if 'email' not in st.session_state:
                    st.session_state['email'] = None
                st.session_state['abbreviation'] = get_abbreviation(st.session_state["username"])
                st.session_state['email'] = get_email(st.session_state["username"])
                
                st.session_state['name'] = get_name(st.session_state["username"])
                
                st.subheader('Account Information')
                org_name = st.text_input('**Organization Name**', value=st.session_state['name'])
                
                cols = st.columns(2)
                username = cols[1].text_input('**Username**', value=st.session_state["username"], disabled=True, help='Username cannot be changed.')
                abbreviation = cols[0].text_input('**Abbreviation**', value=st.session_state['abbreviation'])
                email = st.text_input('**Email**', value=get_email(st.session_state["username"]), disabled=True, help='Email can be changed at the "Update Email Address" tab.')

                fields_blank = (
                    not org_name or org_name.strip() == '' or
                    not abbreviation or abbreviation.strip() == ''
                )
                
                # Dictionary to track changed fields and their new values
                changed_fields = {}

                # Check if each field has changed and update the dictionary
                if org_name != st.session_state['name']:
                    changed_fields['Organization Name'] = org_name
                if abbreviation != st.session_state['abbreviation']:
                    changed_fields['Abbreviation'] = abbreviation
                
                fields_changed = bool(changed_fields)
            
                update_records = st.button('Save', disabled=fields_blank or not fields_changed)
                if update_records:
                    updated_fields = []
                    
                    msg = st.toast('Updating Records...', icon='🔄')
                    for field, new_value in changed_fields.items():
                        # Run the modify_user_data function for each changed field
                        if field == 'Organization Name':
                            affected_rows = modify_user_data("username", "org_name", st.session_state["username"], new_value)
                        else:
                            affected_rows = modify_user_data("username", field, st.session_state["username"], new_value)
                        
                        if affected_rows > 0:
                            updated_fields.append(field)
                    time.sleep(1)
                    msg.toast('Records Updated!', icon='✅')
                    time.sleep(1)
                    if updated_fields:
                        st.session_state['abbreviation'] = get_abbreviation(st.session_state["username"])
                        st.session_state['email'] = get_email(st.session_state["username"])
                        st.session_state['name'] = org_name
                        if len(updated_fields) == 1:
                            success_message = f"{updated_fields[0]} has been successfully changed."
                        elif len(updated_fields) == 2:
                            success_message = f"{' and '.join(updated_fields)} have been successfully changed."
                        else:
                            success_message = f"{', '.join(updated_fields[:-1])}, and {updated_fields[-1]} have been changed."

                    sac.alert(label=success_message, size='sm', radius='md', variant='quote-light', color='success', icon=True, closable=True)
                    time.sleep(5)
                

        elif current_tab == 'Update Email Address':
            with st.container(border=True):
                st.subheader('Update Webmail Address')
                email = st.text_input('**Current Webmail Address**', value=st.session_state['email'], disabled=True)
                new_email = st.text_input('**New Webmail Address**', help='Email must end in @iskolarngbayan.pup.edu.ph')
                verify_button = st.button('Verify', 
                                          disabled=not (new_email and new_email.endswith('@iskolarngbayan.pup.edu.ph') and len(new_email) > len('@iskolarngbayan.pup.edu.ph') and new_email != st.session_state['email'] and st.session_state.otp_attempts < 3))
            
                if verify_button:
                    st.session_state.verification_initiated = True

                if st.session_state.verification_initiated and st.session_state.otp_attempts >= 3:
                    sac.alert(label='Too many failed attempts. Please try again later.', size='sm', radius='md', variant='quote-light', color='error', icon=True, closable=True)

                if st.session_state.verification_initiated and st.session_state.otp_attempts < 3:
                    if not st.session_state.otp_sent:
                        st.session_state.generated_otp = random.randint(100000, 999999)
                        send_otp_email(new_email, st.session_state.generated_otp, st.session_state.abbreviation)
                        st.session_state.otp_sent = True

                    st.session_state.entered_otp = st.text_input('Enter OTP')

                    if st.button('Submit'):
                        if str(st.session_state.entered_otp) == str(st.session_state.generated_otp):
                            msg = st.toast('Changing Webmail Address...', icon='🔄')
                            time.sleep(1)
                            msg.toast('Webmail Address Changed!', icon='✅')
                            sac.alert(label=f'Webmail changed to {new_email}', size='sm', radius='md', variant='quote-light', color='success', icon=True, closable=True)
                            st.session_state.otp_sent = False
                            st.session_state.verification_initiated = False
                            st.session_state.otp_attempts = 0 
                        else:
                            st.session_state.otp_attempts += 1
                            st.error('OTP does not match')
                            if st.session_state.otp_attempts >= 3:
                                st.error("Too many failed attempts. Please try again later.")

                    # Display the alert message about OTP being sent
                    if st.session_state.verification_initiated and not st.session_state.otp_sent:
                        sac.alert(label='A one-time passcode will be sent to your new email for verification.', size='sm', radius='sm', variant='quote-light', color='warning', icon=True, closable=True)

        elif current_tab == 'Update Password':
            with st.container(border=True):
                st.subheader('Update Password')
                password = st.text_input('**Old Password**', type='password')
                new_password = st.text_input('**New Password**', type='password')
                confirm_password = st.text_input('**Confirm Password**', type='password')
                st.button('Save', disabled=True)

# add results screen

# disable or unrender save button if no changes were made

# can modify: org name, abbreviation password
# still show other fields but disable

# user - for orgs
# cosoa - for evals
# execcomm - for org assignment
# chair - for admin level access (see all user info and change access