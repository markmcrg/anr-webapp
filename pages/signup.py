import streamlit as st
import streamlit_antd_components as sac
import re
from helpers import register_user, check_email, check_username

def signup():
    st.write('signup page')
    
    if 'page' not in st.session_state:
        st.session_state.page = 1    
    if 'otp' not in st.session_state:
        st.session_state.otp = None
    if 'otp_sent' not in st.session_state:
        st.session_state.otp_sent = False
    
    def next_page():
        st.session_state.page += 1
        st.rerun()

    def prev_page():
        st.session_state.page -= 1
        st.rerun()
    
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
            st.write('Enter OTP')
            otp = st.text_input('OTP')
            if st.button('Submit'):
                if otp == st.session_state.otp:
                    st.success('Account successfully created')
                else:
                    st.error('Invalid OTP')
                    
    if st.session_state.page == 4:
        st.success('Account successfully created')

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
