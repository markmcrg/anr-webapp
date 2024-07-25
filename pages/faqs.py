import streamlit as st
import streamlit_antd_components as sac

def faqs():
    st.markdown("<h1 style='text-align: center;'>Frequently Asked Questions (FAQs)</h1>", unsafe_allow_html=True)

    cols = st.columns([0.4,1,0.4], gap='medium')

    with cols[0]:
        faq_type = sac.buttons([
        sac.ButtonsItem(label='Accreditation'),
        sac.ButtonsItem(label='Revalidation'),
        sac.ButtonsItem(label='Account'),
        sac.ButtonsItem(label='Contact Us',),
    ], align='center', direction='vertical', radius='lg', variant='text')
        
    with cols[1]:
        if faq_type == "Accreditation":
            with st.expander("What is Accreditation?"):
                st.write("Accreditation is the process of evaluating the performance of a student organization based on the criteria set by the Office of Student Services (OSS).")
            with st.expander("What are the benefits of being an accredited organization?"):
                st.write("Accredited organizations are recognized by the Polytechnic University of the Philippines (PUP) and are entitled to various privileges such as financial assistance, use of university facilities, and participation in university-wide activities.")
            with st.expander("How can my organization apply for accreditation?"):
                st.write("To apply for accreditation, your organization must submit the necessary requirements to the OSS. The requirements include the Certificate of Recognition from the Central/Local Student Council, the organization's Constitution and Bylaws, and the General Plan of Activities with Budgetary Outlay.")
            with st.expander("How long is the accreditation valid?"):
                st.write("The accreditation is valid for one academic year and must be renewed annually.")
            with st.expander("What is the difference between accreditation and revalidation?"):
                st.write("Accreditation is the initial evaluation of a student organization, while revalidation is the renewal of the organization's accreditation.")
                
        elif faq_type == "Revalidation":
            with st.expander("What is Revalidation?"):
                st.write("Revalidation is the process of renewing the accreditation of a student organization based on the criteria set by the Office of Student Services (OSS).")
            with st.expander("What are the requirements for revalidation?"):
                st.write("The requirements for revalidation include the Certificate of Recognition from the Central/Local Student Council, the organization's Constitution and Bylaws, and the General Plan of Activities with Budgetary Outlay.")
            with st.expander("How often does my organization need to undergo revalidation?"):
                st.write("Organizations must undergo revalidation annually to maintain their accredited status.")
            with st.expander("What happens if my organization fails to undergo revalidation?"):
                st.write("Organizations that fail to undergo revalidation will lose their accredited status and will not be entitled to the privileges of an accredited organization.")
            with st.expander("Can my organization apply for revalidation if it has been inactive for a semester?"):
                st.write("Organizations that have been inactive for a semester may apply for revalidation, but they must submit additional requirements to prove that they are still active.")
                
        elif faq_type == "Account":
            with st.expander("How can I create an account?"):
                st.write("To create an account, click on the 'Sign Up' button on the login page and fill out the required information.")
            with st.expander("I forgot my password. What should I do?"):
                st.write("If you forgot your password, click on the 'Forgot Password' link on the login page and follow the instructions to reset your password.")
            with st.expander("How can I update my account information?"):
                st.write("To update your account information, log in to your account and click on the 'Profile' tab to edit your information.")
            with st.expander("How can I delete my account?"):
                st.write("To delete your account, send an email to the support team with your request.")
                
        elif faq_type == "Contact Us":
            with st.expander("How can I contact the Office of Student Services (OSS)?"):
                st.write("You can contact the OSS through the following channels:")
                st.write("- Email: studentservices@pup.edu.ph")
            with st.expander("How can I report a technical issue?"):
                st.write("To report a technical issue, send an email to the support team with a detailed description of the problem.")
            with st.expander("How can I provide feedback or suggestions?"):
                st.write("To provide feedback or suggestions, send an email to the support team with your comments.")
            with st.expander("How can I request a feature or enhancement?"):
                st.write("To request a feature or enhancement, send an email to the support team with your request.")
            