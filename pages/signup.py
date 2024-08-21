import streamlit as st
import streamlit_antd_components as sac
import re
import random
from helpers import register_user, check_email, check_username, send_otp_email

def signup():
    if 'page' not in st.session_state:
        st.session_state.page = 1    
    if 'entered_otp' not in st.session_state:
        st.session_state.entered_otp = None
    if 'otp_sent' not in st.session_state:
        st.session_state.otp_sent = False
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

    def next_page():
        st.session_state.page += 1
        st.rerun()

    def prev_page():
        st.session_state.page -= 1
        st.rerun()
    sac.steps(
            items=[
            sac.StepsItem(title='Register', disabled=True),
            sac.StepsItem(title='Confirm DPA', disabled=True),
            sac.StepsItem(title='Verify Email', disabled=True),
            sac.StepsItem(title='Account Created', disabled=True, icon="check-circle"),
        ], return_index=True, placement='vertical', index=st.session_state.page-1
    ) 
    # Registration Form Page
    if st.session_state.page == 1:
        

        with st.container(border=True):
            sac.divider(label='Signup', icon='clipboard', align='center', color='gray')
            
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

            
            register = st.button('Register', disabled=not all_fields_filled)
    
            if register:
                # Check if password is strong
                if not is_strong_password(password):
                    st.error('Password must be at least 8 characters long, with at least one uppercase letter, one lowercase letter, one number, and one special character')
                elif not password_match:
                    st.error('Passwords do not match')
                elif not valid_email:
                    st.error('Email must end in @iskolarngbayan.pup.edu.ph')
                else:
                    # Check if username is unique
                    if check_username(username):
                        st.error('Username already exists')
                    elif check_email(email):
                        st.error('Email already exists')
                    else:
                        # assign all variables to session state
                        st.session_state.org_name = org_name
                        st.session_state.username = username
                        st.session_state.abbreviation = abbreviation
                        st.session_state.email = email
                        st.session_state.password = password    
                        next_page()
    # DPA Page
    if st.session_state.page == 2:       
        st.header('Data Privacy Act of 2012')
        with st.container(border=True):
            st.write("In accordance with Republic Act No. 10173, otherwise known as the Data Privacy Act of 2012, in answering this form and disclosing your personal information, you consent PUP SC COSOA to access, collect, and process any personal information you encoded. The information gathered will be handled with reasonable and appropriate security measures to maintain the confidentiality of your personal data. By clicking 'I Agree', you acknowledge that you have read and understood the Data Privacy Act of 2012 and consent to the processing of your personal information.")
            if st.button('I Agree'):
                next_page()

    # OTP Page            
    if st.session_state.page == 3:
        with st.container(border=True):
            st.write(f'A One-Time Passcode (OTP) has been sent to your email at *{st.session_state.email}*. Please enter the OTP below to verify your account.')
            
            # Generate random OTP if not yet sent
            if not st.session_state.otp_sent:
                st.session_state.generated_otp = random.randint(100000, 999999)
                send_otp_email(st.session_state.email, st.session_state.generated_otp, st.session_state.abbreviation)
                st.session_state.otp_sent = True
                
            st.session_state.entered_otp = st.text_input('Enter OTP')
                
            if st.button('Submit'):
                if str(st.session_state.entered_otp) == str(st.session_state.generated_otp):
                    st.session_state.otp_sent = False
                    next_page()
                else:
                    st.error('OTP does not match')
                    
    if st.session_state.page == 4:
        if register_user(st.session_state.email, st.session_state.password, st.session_state.org_name, st.session_state.username, st.session_state.abbreviation):
            sac.result(label='Registration Successful!', description='You may know login to your account.', status='success')
        else:
            sac.result(label='Registration Unsuccessful :(', description='Please try again, and if the error persists, please contact us.', status='error')
signup()

# Add timeline - 1. Register, 2. DPA, 3. OTP, 4. Success
# FORM VALIDATION:
# 1. Check if password and confirm password match - done
# 2. Check for DPA - done
# 3. Check if all fields are filled - done
# 4. Check if email is valid (must end in @iskolarngbayan.pup.edu.ph) - done
# 5. Check if password is strong (at least 8 characters long, with at least one uppercase letter, one lowercase letter, one number, and one special character) - done
# 6. Check if username is unique - done
# 7. Check if email is unique - done

