import streamlit as st
import streamlit_antd_components as sac
import time
from helpers import authenticate_b2, get_download_url, upload_document, modify_user_data, get_app_orders, get_app_type, record_submission, get_abbreviation, fetch_data

def accreditation_application():
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

    def prev_step():
        st.session_state.current_step -= 1
        st.rerun()
    
    page_cols = st.columns([0.15, 1, 0.15], vertical_alignment='center')
    
    with page_cols[1]:
        with st.container(border=True, key='step_cont'):
            st.session_state.current_step = sac.steps(
                items=[
                    sac.StepsItem(title='Application', disabled=st.session_state.step_1_disabled),
                    sac.StepsItem(title='Organization', disabled=st.session_state.step_2_disabled),
                    sac.StepsItem(title='Upload', disabled=st.session_state.step_3_disabled),
                    sac.StepsItem(title='Confirm', disabled=st.session_state.step_4_disabled),
                    sac.StepsItem(title='Submitted!', disabled=st.session_state.step_5_disabled, icon='check-circle-fill'),
                ], return_index=True, placement='vertical', direction='horizontal', variant='navigation', index=st.session_state.current_step
            )
    
    if st.session_state.current_step == 0:
        # Fetch data here from settings table to check if accepting_responses is True and if accepting_resubmissions is True
        settings = fetch_data('https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_settings')['data']['rows']
        # if accepting submissions is False, show a screen that says "We are currently not accepting applications at the moment. Please check back later."
        if settings[1]['status'] == "TRUE":
            # if accepting resubmissions is False, show a screen that says "We are currently not accepting new submissions at the moment. Please check back later."
            with page_cols[1]:
                with st.container(border=True, key='accre_cont'):
                    st.session_state.current_step = 0
                    st.session_state.step_1_disabled = False
                    # st.write("")
                    # st.markdown("<h4 style='text-align: center;'>1. Select your application type, and the order of your application.</h4><br><br>", unsafe_allow_html=True)
                    # st.write("")
                    cols = st.columns([0.2, 1,1, 0.2], gap='small', vertical_alignment='center')

                    # Check if user has submitted an application before
                    accre_disabled = False
                    reval_disabled = False
                    app_type = get_app_type(st.session_state['username'])
                    
                    if app_type == "Accreditation":
                        reval_disabled = True
                    elif app_type == "Revalidation":
                        accre_disabled = True
                        
                    app_orders = get_app_orders(st.session_state['username'])
                    
                    with cols[1]:
                        with st.container(border=True):
                            st.session_state.app_type = sac.buttons([
                                sac.ButtonsItem(label='Accreditation', icon='check2-circle', disabled=accre_disabled),
                                sac.ButtonsItem(label='Revalidation', icon='arrow-repeat', disabled=reval_disabled),
                            ], label='', direction='vertical', gap='md', variant='outline', use_container_width=True, align='center', size='md', index=2)
                    with cols[2]:
                        with st.container(border=True):
                            st.session_state.app_order = sac.buttons([
                                sac.ButtonsItem(label='Initial Submission', icon='1-circle', disabled=True if int(app_orders['initial_sub']) == 1 or settings[0]['status'] == "FALSE" else False),
                                sac.ButtonsItem(label='1st Resubmission', icon='2-circle', disabled=True if int(app_orders['first_resub']) == 1 else False),
                                sac.ButtonsItem(label='2nd Resubmission', icon='3-circle', disabled=True if int(app_orders['second_resub']) == 1 else False),
                            ], label='', direction='vertical', gap='md', variant='outline', use_container_width=True, align='center', size='md', index=3)
                    next_btn = st.button("Next", key="next", disabled= not (st.session_state.app_type and st.session_state.app_order))
                    if settings[0]['status'] == "FALSE":
                        sac.alert(label='Initial submissions are closed. Proceed with your application only if you have submitted your initial submission.', size='sm', variant='quote-light', color='info', icon=True)
                    if next_btn:
                        next_step()
        else:
            with page_cols[2]:
                with st.container(border=True):
                    sac.result(label='Submissions closed.', description='We are currently not accepting applications at the moment. Please check back later.', status="info")
    if st.session_state.current_step == 1:
        st.session_state.current_step = 1
        st.session_state.step_2_disabled = False
        with page_cols[1]:
            with st.container(border=True):
                abbreviation = get_abbreviation(st.session_state['username'])
                st.session_state.org_abbrv = f'{st.session_state["name"]} ({abbreviation})'
                st.text_input("**Complete Name of Student Organization (Abbreviation/Initialism)**", placeholder="PowerPuff Girls Ensemble (PPGE)", 
                                        value=st.session_state.org_abbrv, 
                                        disabled=True, 
                                        help='To modify this, please change your details in Account Settings.')
                jurisdictions = {
                    "University-Wide (U-Wide)": "U-WIDE",
                    "College of Architecture, Design, and the Built Environment (CADBE)": "CADBE",
                    "College of Accountancy and Finance (CAF)": "CAF",
                    "College of Arts and Letters (CAL)": "CAL",
                    "College of Business Administration (CBA)": "CBA",
                    "College of Computer and Information Sciences (CCIS)": "CCIS",
                    "College of Engineering (CE)": "CE",
                    "College of Human Kinetics (CHK)": "CHK",
                    "College of Communication (COC)": "COC",
                    "College of Education (COED)": "COED",
                    "College of Political Science and Public Administration (CPSPA)": "CPSPA",
                    "College of Science (CS)": "CS",
                    "College of Social Sciences and Development (CSSD)": "CSSD",
                    "College of Tourism, Hospitality, and Transportation Management (CTHTM)": "CTHTM",
                    "Insititute of Technology (ITech)": "ITECH",
                    "Open University System (OUS)": "OUS",
                    "Graduate School (GS)": "GS",
                    "Lab High School (LHS)": "LHS",
                    "Senior High School (SHS)": "SHS"
                }

                jurisdiction = st.selectbox("**Jurisdiction**", list(jurisdictions.keys()), 
                                            help='This is where your organization and its members will be based.')

                st.session_state.jurisdiction = jurisdictions[jurisdiction] if jurisdiction else None
                    
                next_btn = st.button("Next", key="next2")
            if next_btn:
                next_step()
    if st.session_state.current_step == 2:
        st.session_state.current_step = 2
        st.session_state.step_3_disabled = False
        with page_cols[1]:
            with st.container(border=True):
                st.session_state.org_doc = st.file_uploader("Upload your document compilation here:", type=['pdf'], help='Please upload your document compilation in PDF format.', label_visibility='visible')
                next_btn = st.button("Next", key="next3", disabled= not st.session_state.org_doc)
        
                if st.session_state.org_doc is not None:
                    sac.alert(label='File uploaded successfully.', size='sm', variant='quote-light', color='success', icon=True)
                
            if next_btn:
                next_step()
                
    if st.session_state.current_step == 3:
        st.session_state.current_step = 3
        st.session_state.step_4_disabled = False
        with page_cols[1]:
            with st.container(border=True):
                st.write(f"**Organization:** {st.session_state.org_abbrv}")
                st.write(f"**Jurisdiction:** {st.session_state.jurisdiction}")
                st.write(f"**Application Type:** {st.session_state.app_type}")
                st.write(f"**Application Order:** {st.session_state.app_order}")
                sac.alert(label='After submission, edits will no longer be possible. Please review your entries carefully.', size='sm', variant='quote-light', color='warning', icon=True)
                submit_btn = st.button("Submit Application", key="submit")
            if submit_btn:
                msg = st.toast('Submitting Application...', icon='⬆️')
                
                # Upload document to B2
                bucket = authenticate_b2('anr-webapp')
                filename = f'{st.session_state.org_abbrv} - {st.session_state.app_order}'
                file_ver = upload_document(bucket, st.session_state.org_doc, filename)
            
                # Modify table app type
                modify_user_data('username', 'app_type', st.session_state.username, st.session_state.app_type)
                # Modify table app order
                if st.session_state.app_order == 'Initial Submission':
                    modify_user_data('username', 'initial_sub', st.session_state.username, 1)
                elif st.session_state.app_order == '1st Resubmission':
                    modify_user_data('username', 'first_resub', st.session_state.username, 1)
                elif st.session_state.app_order == '2nd Resubmission':
                    modify_user_data('username', 'second_resub', st.session_state.username, 1)
                
                
                # Get link of doc from server
                b2_pdf_url = get_download_url(bucket, filename + '.pdf', auth=False)
                record_submission(filename,
                                st.session_state.org_abbrv,
                                st.session_state.app_type,
                                st.session_state.app_order,
                                st.session_state.jurisdiction,
                                b2_pdf_url,
                                st.session_state.username)
                
                if file_ver and b2_pdf_url:
                    msg.toast('Application submitted successfully!', icon='🎉')
                    time.sleep(1)
                    next_step()
                
    if st.session_state.current_step == 4:
        st.session_state.current_step = 4
        for i in range(1, 6):
            st.session_state[f'step_{i}_disabled'] = True
        with page_cols[1]:
            sac.result(label='Application Submitted!', description='Please check the status of your submission by clicking on "Accreditation Status."', status='success')
            
        # delete org doc from st state
        del st.session_state['org_doc']

            
    # TODO:
    # - second to the Last page: add dpa, waiver of responsibility, and submit button
    # page basis
    # lock jursidiction after initial submission with message?