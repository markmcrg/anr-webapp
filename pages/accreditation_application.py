import streamlit as st
import streamlit_antd_components as sac

st.markdown("<h1 style='text-align: center;'>Accreditation Application</h1>", unsafe_allow_html=True)
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
current_step = sac.steps(
    items=[
        sac.StepsItem(title='Organization Info', subtitle='Provide the necessary information about your organization.', disabled=True),
        sac.StepsItem(title='Upload Forms', subtitle='Upload the required forms for accreditation.',    ),
        sac.StepsItem(title='Confirm Application', subtitle='Review and confirm your application.',),
    ], color='maroon', return_index=True, placement='vertical'
)
st.write("---")
cols = st.columns([0.4,1,0.4])
if current_step == 0:
    
    with cols[1]:
        st.header("Organization Info")
        org_name = st.text_input("Complete Name of Student Organization (Abbreviation/Initialism)", placeholder="PowerPuff Girls Ensemble (PPGE)")
        jurisdiction = st.selectbox("Jurisdiction", ["University-Wide (U-Wide)", "College of Architecture, Design, and the Built Environment (CADBE)", "College of Accountancy and Finance (CAF)", "College of Arts and Letters (CAL)", "College of Business Administration (CBA)", "College of Computer and Information Sciences (CCIS)", "College of Engineering (CE)", "College of Human Kinetics (CHK)", "College of Communication (COC)", "College of Education (COED)", "College of Political Science and Public Administration (CPSPA)", "College of Science (CS)", "College of Social Sciences and Development (CSSD)", "College of Tourism, Hospitality, and Transportation Management (CTHTM)", "Insititute of Technology (ITech)", "Open University System (OUS)", "Graduate School (GS)", "Lab High School (LHS)", "Senior High School (SHS)"])
    
# TODO:
# - Last page: add dpa, waiver of responsibility, and submit button