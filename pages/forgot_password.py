import streamlit as st
import streamlit_antd_components as sac
from helpers import modify_user_data, send_otp_email, get_abbreviation_from_webmail
import random
import re
import time
import hydralit_components as hc
def forgot_password():
    with hc.HyLoader('',hc.Loaders.standard_loaders,index=[2]):
        if 'entered_otp' not in st.session_state:
            st.session_state.entered_otp = None
        if 'otp_sent' not in st.session_state:
            st.session_state.otp_sent = False
        if 'generated_otp' not in st.session_state:
            st.session_state.generated_otp = None
        if 'fp_page' not in st.session_state:
            st.session_state.fp_page = 1 
        if 'webmail' not in st.session_state:
            st.session_state.webmail = None
        if 'abbreviation' not in st.session_state:
            st.session_state.abbreviation = None    

        def next_page():
            st.session_state.fp_page += 1
            st.rerun()

        def prev_page():
            st.session_state.fp_page -= 1
            st.rerun()
            
        cols = st.columns([0.3, 1, 0.3], vertical_alignment='center')
        if st.session_state.fp_page == 1:
            with cols[1]:
                with st.container(border=True):
                    st.subheader("Reset Password")
                    st.session_state.webmail = st.text_input('Webmail Address', help='Webmail must end in @iskolarngbayan.pup.edu.ph', autocomplete='email')
                    sac.alert(label='Once you click submit, a one-time passcode (OTP) will be sent to your entered email.', size='sm', variant='quote-light', icon=True)
                    
                    if st.button("Submit", disabled= not st.session_state.webmail):
                        st.session_state.abbreviation= get_abbreviation_from_webmail(st.session_state.webmail)
                        
                        if st.session_state.abbreviation:
                            next_page()
                        else:
                            sac.alert(label='Invalid webmail. Please try again.', size='sm', variant='quote-light', icon=True, color='error')

        elif st.session_state.fp_page == 2:
            with cols[1]:
                with st.container(border=True):
                    st.subheader("Reset Password")
                    
                    if not st.session_state.otp_sent:
                        st.session_state.generated_otp = random.randint(100000, 999999)
                        send_otp_email(st.session_state.webmail, st.session_state.generated_otp, st.session_state.abbreviation)
                        st.session_state.otp_sent = True
                        
                    st.session_state.entered_otp = st.text_input('Enter One-time Passcode (OTP)')
                    
                    sac.alert(label=f'A One-Time Passcode (OTP) has been sent to your email at *{st.session_state.webmail}*.', size='sm', variant='quote-light', icon=True)
                    
                    if st.button("Verify", disabled= not st.session_state.webmail):
                        if str(st.session_state.entered_otp) == str(st.session_state.generated_otp):
                            st.session_state.otp_sent = False
                            next_page()
                        else:
                            sac.alert(label='Invalid OTP. Please try again.', size='sm', variant='quote-light', icon=True, color='error')
        elif st.session_state.fp_page == 3:
            with cols[1]:
                with st.container(border=True):
                    st.subheader("Reset Password")
                    password = st.text_input('New Password', type='password', help='Password must be at least 8 characters long, with at least one uppercase letter, one lowercase letter, one number, and one special character')
                    confirm_password = st.text_input('Confirm New Password', type='password', help='Re-enter your password')
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
                    
                    if st.button("Submit", disabled= not password or not confirm_password):
                        if not is_strong_password(password):
                            sac.alert(label='Password must be at least 8 characters long, with at least one uppercase letter, one lowercase letter, one number, and one special character', size='sm', variant='quote-light', icon=True, color='warning')
                        elif not password == confirm_password:
                            sac.alert(label='Passwords do not match.', size='sm', variant='quote-light', icon=True, color='warning')
                        elif not password or not confirm_password:
                            sac.alert(label='Please fill in all fields.', size='sm', variant='quote-light', icon=True, color='warning')
                        elif password == confirm_password:
                            st.toast('Changing password...', icon="🔃")
                            affected_rows = modify_user_data('email', 'password', st.session_state.webmail, password)
                            if affected_rows == 1:
                                time.sleep(2)
                                next_page()
                            else:
                                sac.alert(label='An error occurred. Please change your password and try again.', size='sm', variant='quote-light', icon=True, color='error')
                        else:
                            sac.alert(label='An error occurred. Please try again.', size='sm', variant='quote-light', icon=True, color='error')
        elif st.session_state.fp_page == 4:
            with cols[1]:
                with st.container():
                    st.toast('Password successfully changed!', icon="✅")
                    sac.result(label='Password successfully changed!', description='You may now login using your new password.', status='success')