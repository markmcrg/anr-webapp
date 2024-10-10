import streamlit as st
import streamlit_antd_components as sac

def faqs():
    st.markdown("<h1 style='text-align: center;'>Frequently Asked Questions (FAQs)</h1>", unsafe_allow_html=True)

    cols = st.columns([0.4,1,0.4], gap='medium')

    with cols[0]:
        faq_type = sac.buttons([
        sac.ButtonsItem(label='Accreditation'),
        sac.ButtonsItem(label='Revalidation'),
        sac.ButtonsItem(label='General'),
        sac.ButtonsItem(label='Fundraising'),
        sac.ButtonsItem(label='Account'),
        sac.ButtonsItem(label='Contact Us',)
    ], align='center', direction='vertical', radius='lg', variant='text')
        
    with cols[1]:
        if faq_type == "Accreditation":
            with st.expander("**What is Accreditation?**"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            with st.expander("**What are the benefits of being an accredited organization?**"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            with st.expander("**How can my organization apply for accreditation?**"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            with st.expander("**How long is the accreditation valid?**"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            with st.expander("**What is the difference between accreditation and revalidation?**"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
                
        elif faq_type == "Revalidation":
            with st.expander("What is Revalidation?"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            with st.expander("What are the requirements for revalidation?"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            with st.expander("How often does my organization need to undergo revalidation?"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            with st.expander("What happens if my organization fails to undergo revalidation?"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            with st.expander("Can my organization apply for revalidation if it has been inactive for a semester?"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
                
        elif faq_type == "Account":
            with st.expander("How can I create an account?"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            with st.expander("I forgot my password. What should I do?"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            with st.expander("How can I update my account information?"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            with st.expander("How can I delete my account?"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
                
        elif faq_type == "Contact Us":
            with st.expander("How can I contact the Office of Student Services (OSS)?"):
                st.write("You can contact the OSS through the following channels:")
                st.write("- Email: studentservices@pup.edu.ph")
            with st.expander("How can I report a technical issue?"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            with st.expander("How can I provide feedback or suggestions?"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            with st.expander("How can I request a feature or enhancement?"):
                st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        elif faq_type == "Fundraising":
            with st.expander("Can we organize fundraising activities now? What are the guidelines for these?"):
                st.write("Yes, as per Executive Order No. 12, Series of 2024, the University President issued the regulation of fund-raising activities and collection activities to all accredited student organizations. You may view the Revised Guidelines and Required Documents through this hyperlink. https://bit.ly/ExecutiveOrder12Series2024")
            with st.expander("What are the required documents that we must submit to collect membership fees?"):
                st.write("Kindly consult with the Office of Student Services (OSS) to ensure updated guidelines and requirements for collecting membership fees.")
            with st.expander("What is the maximum amount that we could collect for the membership fee?"):
                st.write("According to Title 7, Section 13.3 of the 2019 PUP Student handbook, an organization's membership fee shall not be more than Fifty Pesos (Php 50.00) per semester.")
            with st.expander("Are we allowed to collect membership fees?"):
                st.write("Yes.")
            with st.expander("If we want our organization to have shirts and/or lanyards, do we still have to process documents, and what are those? Is it counted as a fundraising activity?"):
                st.write("If there is no profit, it is not counted as a fundraising activity. There are no documents needed, however, please consult with PUP SC COA regarding the organization’s Financial Statements.")
        elif faq_type == "General":
            with st.expander(" How long do we have to wait until we receive an email regarding the documents we have submitted?"):
                st.write("All lapses found in the documents will be sent through an email within twelve (12) calendar days from the next Monday it was submitted.")
            with st.expander("Shall we wait for the email from PUP SC COSOA containing notes regarding our previous submission before submitting another set of documents?"):
                st.write("Yes.")
            with st.expander("After correcting our previous lapses and resubmitting our documents, is there an assurance that our organization’s documents don’t have lapses and are already subjected to accreditation/revalidation approval?"):
                st.write("The Office of the Chairperson will release a memorandum stating the organizations that passed the COSOA Chairperson’s Approval and will be endorsed to the Office of Student Services (OSS).")
            with st.expander("Is it required to put our organization’s letterhead on our documents?"):
                st.write("No, it is optional. However, keep in mind that if the letterhead of a document is from the Commission, you are prohibited from removing or editing it.")
            with st.expander("Is it fine if we do not put any attachments on our Accomplishment Report?"):
                st.write("Attachments (e.g., list of attendees, members, etc.) are not required, but you should put at least three (3) pieces of documentation (e.g., screenshots, event receipts, etc.)")
            with st.expander("Are there any documents we can submit as an alternative to the Certificate of Registration that don’t have a QR code?"):
                st.write("You may submit either your PUPSIS-generated First Semester confirmation slip, Certificate of Enrollment, or class schedule.")
            with st.expander("Are we allowed to put “SGD” for the signatories’ part instead of our e-signatures?"):
                st.write("No, all documents must be signed.")
            with st.expander("For the Accomplishment Report, if the officer with the highest rank (e.g., President) was the one who prepared this document, whom shall we put on the signatory of approval?"):
                st.write("The next highest-ranking officer.")
            with st.expander("For the General Plan of Activities (GPOA), under the month column, should we include the year (e.g., December 2022) based on the given accomplished templates?"):
                st.write("Yes.")
            with st.expander("What are the guidelines for conducting on-site activities/programs?"):
                st.write("Kindly contact us at our webmail (cosoa@iskolarngbayan.pup.edu.ph) or at our official Facebook page (link here) for more information.")
            
           
faqs()