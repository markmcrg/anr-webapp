import streamlit as st
import streamlit_antd_components as sac
import re
import random
import streamlit_shadcn_ui as ui
# Add the main directory to the system path if necessary
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers import register_user, check_email, check_username, send_otp_email
from streamlit_extras.stylable_container import stylable_container
import time

def signup():
    cols = st.columns([0.25, 1, 0.25])
    with cols[1]:
        if 'page' not in st.session_state:
            st.session_state.page = 1    
        if 'entered_otp' not in st.session_state:
            st.session_state.entered_otp = None
        if 'generated_otp' not in st.session_state:
            st.session_state.generated_otp = None
        if 'org_name' not in st.session_state:
            st.session_state.org_name = None
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'abbreviation' not in st.session_state:
            st.session_state.abbreviation = None
        if 'email' not in st.session_state:
            st.session_state.email = None
        if 'password' not in st.session_state:
            st.session_state.password = None
        if 'dpa_agree' not in st.session_state:
            st.session_state.dpa_agree = False 

        def next_page():
            st.session_state.page += 1
            st.rerun()

        def prev_page():
            st.session_state.page -= 1
            st.rerun()
            
        st.markdown("<h1 style='text-align: center; color: #f5c472; font-size: 45px; padding-bottom:25px;'>Sign Up</h1>", unsafe_allow_html=True)
        st.markdown("""
                    <style>
                    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stMain.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stMainBlockContainer.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div.stHorizontalBlock.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.stColumn.st-emotion-cache-115gedg.e1f1d6gn3 > div > div > div > div:nth-child(3) > div > div > div {
                        padding-top: 20px;
                    }
                    #sign-up {
                        margin-bottom: -0.75em;
                    }
                    </style>
                    """, unsafe_allow_html=True)
        with st.container(border=True, key='step_container'):
            sac.steps(
                    items=[
                    sac.StepsItem(title='Register', disabled=True),
                    # sac.StepsItem(title='Confirm DPA', disabled=True),
                    sac.StepsItem(title='Verify', disabled=True),
                    sac.StepsItem(title='Success!', disabled=True, icon="check-circle"),
                ], return_index=True, placement='vertical', index=st.session_state.page-1, key='signup_steps'
            ) 
            # Registration Form Page
        with st.container(border=True):
            if st.session_state.page == 1:
                with st.container(border=False):
                    org_name = st.text_input('Organization Name', placeholder='PUP Student Council Commission on Student Organizations and Accreditation')
                    cols = st.columns(2)
                    username = cols[0].text_input('Username', help='Username must be unique', max_chars=20, placeholder='pupsccosoa')
                    abbreviation = cols[1].text_input('Organization Abbreviation/Initialism', placeholder='PUP SC COSOA')
                    email = st.text_input('PUP Organization/Representative Webmail', placeholder='cosoa@iskolarngbayan.pup.edu.ph', help='Email must end in @iskolarngbayan.pup.edu.ph')
                    password = st.text_input('Password', type='password', help='Password must be at least 8 characters long, with at least one uppercase letter, one lowercase letter, one number, and one special character')
                    confirm_password = st.text_input('Confirm Password', type='password', help='Re-enter your password')

                    all_fields_filled = org_name and username and abbreviation and email and password and confirm_password
                    password_match = password == confirm_password
                    valid_email = email.endswith('@iskolarngbayan.pup.edu.ph')
                    existing_username = check_username(username)
                    existing_email = check_email(email)
                    
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
                        if not re.search(r'[!@#$%^&*(),.?":{}|<>_]', password):
                            return False
                        return True

                    
                    register = ui.button(text="Register", key="register", className="bg-red-900 text-white")
                    show_state = register and all_fields_filled and password_match and valid_email and not existing_username and not existing_email and is_strong_password(password)
                    st.session_state.dpa_agree = ui.alert_dialog(show=show_state, title="Data Privacy Act of 2012", description="In accordance with Republic Act No. 10173, otherwise known as the Data Privacy Act of 2012, in answering this form and disclosing your personal and organizational information, you consent PUP SC COSOA to access, collect, and process any information you encoded. The information gathered will be handled with reasonable and appropriate security measures to maintain the confidentiality of your personal data. By clicking 'I Agree', you acknowledge that you have read and understood the Data Privacy Act of 2012 and consent to the processing of your personal information.", confirm_label="I agree", cancel_label="Cancel", key="dpa_dialog")


                    if register:
                        # Check if password is strong
                        if not all_fields_filled:
                            sac.alert(label='Please fill in all fields.', size='sm', variant='quote-light', color='error', icon=True)
                        elif not is_strong_password(password):
                            sac.alert(label='Password must be at least 8 characters long, with at least one uppercase letter, one lowercase letter, one number, and one special character.', size='sm', variant='quote-light', color='error', icon=True)
                        elif not password_match:
                            sac.alert(label='Passwords do not match.', size='sm', variant='quote-light', color='error', icon=True)
                        elif not valid_email:
                            sac.alert(label='Email must end in @iskolarngbayan.pup.edu.ph.', size='sm', variant='quote-light', color='error', icon=True)
                        elif existing_username:
                            sac.alert(label='Username is already in use by a registered account.', size='sm', variant='quote-light', color='error', icon=True)
                        elif existing_email:
                            sac.alert(label='Email is already in use by a registered account.', size='sm', variant='quote-light', color='error', icon=True)

                        else:
                            # assign all variables to session state
                            st.session_state.org_name = org_name
                            st.session_state.username = username
                            st.session_state.abbreviation = abbreviation
                            st.session_state.email = email
                            st.session_state.password = password    

                            # next_page()
                    if st.session_state.dpa_agree:
                        next_page()
    # # DPA Page
            # if st.session_state.page == 2:       
            #     st.header('Data Privacy Act of 2012')
            #     with st.container(border=True):
            #         st.write("In accordance with Republic Act No. 10173, otherwise known as the Data Privacy Act of 2012, in answering this form and disclosing your personal information, you consent PUP SC COSOA to access, collect, and process any personal information you encoded. The information gathered will be handled with reasonable and appropriate security measures to maintain the confidentiality of your personal data. By clicking 'I Agree', you acknowledge that you have read and understood the Data Privacy Act of 2012 and consent to the processing of your personal information.")
            #         if st.button('I Agree'):
            #             next_page()

            # OTP Page            
            if st.session_state.page == 2:
                with st.container(border=False):
                    st.write(f'A One-Time Passcode (OTP) has been sent to your email at *{st.session_state.email}*. Please enter the OTP below to verify your account.')
                    time.sleep(3)
                    
                    # Generate and send OTP only if it hasn't been sent yet
                    if 'otp_sent' not in st.session_state or not st.session_state.otp_sent:
                        # Generate OTP and send email
                        st.session_state.generated_otp = random.randint(100000, 999999)
                        send_otp_email(st.session_state.email, st.session_state.generated_otp, st.session_state.abbreviation)
                        
                        # Mark OTP as sent
                        st.session_state.otp_sent = True
                        
                    st.session_state.entered_otp = st.text_input('Enter OTP')
                    submit_btn = ui.button(text="Submit", key="submit", className="bg-red-900 text-white")
                    sac.alert(label='Kindly check your spam or junk folder if you don\'t see the OTP email in your inbox.', size='sm', variant='quote-light', color='info', icon=True)
                    if submit_btn:
                        if str(st.session_state.entered_otp) == str(st.session_state.generated_otp):
                            st.session_state.otp_sent = False
                            next_page()
                        else:
                            sac.alert(label='One-Time Passcode does not match.', size='sm', variant='quote-light', color='error', icon=True)
                            
            if st.session_state.page == 3:
                if register_user(st.session_state.email, st.session_state.password, st.session_state.org_name, st.session_state.username, st.session_state.abbreviation):
                    sac.result(label='Registration Successful!', description='You may now log in to your account.', status='success')
                else:
                    sac.result(label='Registration Unsuccessful :(', description='Please try again, and if the error persists, please contact us.', status='error')

# Add timeline - 1. Register, 2. DPA, 3. OTP, 4. Success
# FORM VALIDATION:
# 1. Check if password and confirm password match - done
# 2. Check for DPA - done
# 3. Check if all fields are filled - done
# 4. Check if email is valid (must end in @iskolarngbayan.pup.edu.ph) - done
# 5. Check if password is strong (at least 8 characters long, with at least one uppercase letter, one lowercase letter, one number, and one special character) - done
# 6. Check if username is unique - done
# 7. Check if email is unique - done

if __name__ == "__main__":
    signup()