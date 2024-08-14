import streamlit as st
import random
import re
import time
import streamlit_antd_components as sac
from helpers import get_email, get_abbreviation, modify_user_data, get_name, send_otp_email, get_password

def account_settings():
    if 'entered_otp' not in st.session_state:
        st.session_state.entered_otp = None
    if 'otp_sent' not in st.session_state:
        st.session_state.otp_sent = False
    if 'generated_otp' not in st.session_state:
        st.session_state.generated_otp = None
    if 'verification_initiated' not in st.session_state:
        st.session_state.verification_initiated = False
    if 'otp_attempts' not in st.session_state:
        st.session_state.otp_attempts = 0
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
                    cols[1].text_input('**Username**', value=st.session_state["username"], disabled=True, help='Username cannot be changed.')
                    abbreviation = cols[0].text_input('**Abbreviation**', value=st.session_state['abbreviation'])
                    st.text_input('**Email**', value=get_email(st.session_state["username"]), disabled=True, help='Email can be changed at the "Update Email Address" tab.')

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
                    st.text_input('**Current Webmail Address**', value=st.session_state['email'], disabled=True)
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
                                affected_rows = modify_user_data("username", "email", st.session_state["username"], new_email)
                                if affected_rows == 1:
                                    msg = st.toast('Changing Webmail Address...', icon='🔄')
                                    time.sleep(1)
                                    msg.toast('Webmail Address Changed!', icon='✅')
                                    sac.alert(label=f'Webmail changed to {new_email}', size='sm', radius='md', variant='quote-light', color='success', icon=True, closable=True)
                                    st.session_state.otp_sent = False
                                    st.session_state.verification_initiated = False
                                    st.session_state.otp_attempts = 0 
                                else:
                                    sac.alert(label='An error occurred. Please try again.', size='sm', radius='md', variant='quote-light', color='error', icon=True, closable=True)
                            else:
                                st.session_state.otp_attempts += 1
                                sac.alert(label='OTP does not match.', size='sm', radius='md', variant='quote-light', color='error', icon=True, closable=True)
                                if st.session_state.otp_attempts >= 3:
                                    sac.alert(label='Too many failed attempts. Please try again later.', size='sm', radius='md', variant='quote-light', color='error', icon=True, closable=True)

                        # Display the alert message about OTP being sent
                        if st.session_state.verification_initiated and not st.session_state.otp_sent:
                            sac.alert(label='A one-time passcode will be sent to your new email for verification.', size='sm', radius='sm', variant='quote-light', color='warning', icon=True, closable=True)

            elif current_tab == 'Update Password':
                with st.container(border=True):
                    st.subheader('Update Password')
                    old_password = st.text_input('**Old Password**', type='password')
                    new_password = st.text_input('**New Password**', type='password')
                    confirm_password = st.text_input('**Confirm Password**', type='password')
                    saved_pw = get_password(st.session_state["username"])
                    save_btn = st.button('Save', disabled=not (old_password and new_password and confirm_password))
                    # add logic to check if old password is correct and new password is not the same as the old password
                    def is_strong_password(password):
                        # Check the length of the password
                        if len(password) < 8:
                            return False
                        # Check for at least one uppercase letter
                        if not re.search(r'[A-Z]', password):
                            return False
                        # Check for at least one lowercase letter
                        if not re.search(r'[a-z]', password):
                            return False
                        # Check for at least one number
                        if not re.search(r'[0-9]', password):
                            return False
                        # Check for at least one special character
                        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                            return False
                        return True
                    if save_btn:
                        if new_password == confirm_password:
                            if is_strong_password(new_password):
                                if old_password == saved_pw:
                                    if new_password == old_password or saved_pw == new_password:
                                        sac.alert(label='New password must be different from the old password.', size='sm', radius='md', variant='quote-light', color='error', icon=True, closable=True)
                                    else:
                                        affected_rows = modify_user_data("username", "password", st.session_state["username"], new_password)
                                        if affected_rows == 1:
                                            msg = st.toast('Changing Password...', icon='🔄')
                                            time.sleep(1)
                                            msg.toast('Password Changed!', icon='✅')
                                            sac.alert(label='Password has been successfully changed.', size='sm', radius='md', variant='quote-light', color='success', icon=True, closable=True)
                                else:
                                    sac.alert(label='Old password is incorrect', size='sm', radius='md', variant='quote-light', color='error', icon=True, closable=True)
                            else:
                                sac.alert(label='Password must be at least 8 characters long, with at least one uppercase letter, one lowercase letter, one number, and one special character.', size='sm', radius='md', variant='quote-light', color='error', icon=True, closable=True)
                        else:
                            sac.alert(label='Passwords must match.', size='sm', radius='md', variant='quote-light', color='error', icon=True, closable=True)