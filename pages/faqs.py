import streamlit as st
import streamlit_antd_components as sac

def faqs():
    st.markdown("<h1 style='color: #f5c472; padding-left: 10px'>Frequently Asked Questions (FAQs)</h1>", unsafe_allow_html=True)
    
    with st.container():
        cols = st.columns([0.25,1], gap='medium')
        with cols[0]:
            with st.container(border=True):
                faq_type = sac.buttons([
                sac.ButtonsItem(label='Accreditation'),
                sac.ButtonsItem(label='Revalidation'),
                sac.ButtonsItem(label='General'),
                sac.ButtonsItem(label='Fundraising'),
                sac.ButtonsItem(label='Account'),
                sac.ButtonsItem(label='Contact Us'),
                sac.ButtonsItem(label='COA')
            ], align='center', direction='vertical', radius='lg', variant='text')
        with cols[1]:
            with st.container(border=True):
                if faq_type == "Accreditation":
                    with st.expander("**What is Accreditation?**"):
                        st.write("Accreditation is the process of formally verifying the student organization or formation’s compliance with the University’s established quality standards to ensure its legal status and competency as an entity.")
                    with st.expander("**What are the benefits of being an accredited organization?**"):
                        st.write("Accredited student organizations or formations will gain official recognition and legal status within the University. They will be eligible to receive the necessary support, resources, and opportunity to achieve a fulfilling campus experience. Additionally, accredited student organizations and formations are strongly encouraged to collaborate with other entities (e.g., external or internal affairs) to expand opportunities for all students and enhance participation in university activities and events.")
                    with st.expander("**How can my organization apply for accreditation?**"):
                        st.write("Aspiring student organizations and formations within the Polytechnic University of the Philippines (PUP) may undergo accreditation by completing the application requirements (refer to the list provided in the “Application Requirements” tab > Accreditation)")
                        
                        st.write("To proceed with the application, create an account and log in to the website. Once logged in, head to the “Accreditation Applications” tab and fill out the information needed from the student organization/formation. Finally, upload the necessary documents and confirm the application!")
                        
                        st.write("The status of the student organization’s Accreditation application can be reviewed under the “Accreditation Status” tab.")
                    with st.expander("**How long is the accreditation valid?**"):
                        st.write("The accreditation remains valid for one (1) academic year or until the Commission releases a new list of accredited student organizations and formations.")
                    with st.expander("**What is the difference between accreditation and revalidation?**"):
                        st.write("Accreditation is for newly formed student organizations or those that have been dormant for three (3) consecutive years. Meanwhile, revalidation is for student organizations with a continuous accreditation/revalidation record for the past two (2) AnR periods.")
                        
                elif faq_type == "Revalidation":
                    with st.expander("**What is Revalidation?**"):
                        st.write("Revalidation is the process of formally renewing the student organization or formation’s legal status within the University by evaluating and assessing its performance data from the previous academic year to ensure its ongoing competency as an entity.")
                    with st.expander("**How often does my organization need to undergo revalidation?**"):
                        st.write("Student organizations and formations are required to undergo revalidation annually.")
                    with st.expander("**What happens if my organization fails to undergo revalidation?**"):
                        st.write("Student organizations and formations that do not revalidate can apply for the next AnR period.")
                    with st.expander("**Can my organization apply for revalidation if it has been inactive for a semester?**"):
                        st.write("Yes, student organizations and formations can still apply for revalidation if they have not been dormant for three (3) consecutive years. Otherwise, they must undergo the full accreditation process.")
                        
                elif faq_type == "Account":
                    with st.expander("**How can I create an account?**"):
                        st.write("To create an account, click the “Sign Up” tab, enter the student organization or formation’s details, and use an already-existing PUP Organization webmail. If a PUP Student Organization/Formation webmail is not available, you may use the Student Organization Representative’s (SOR) webmail. ")
                    with st.expander("**I forgot my password. What should I do?**"):
                        st.write("Under the “Password Reset” tab, enter the webmail address you used to sign up. A one-time passcode (OTP) will be sent to your registered email address. Wait for its arrival and enter it to proceed.")
                    with st.expander("**How can I update my account information?**"):
                        st.write("Log in to your account, then update any necessary information (Profile, Email Address, and Password) via the “Account Settings” tab. Save your changes when finished.")
                    with st.expander("**How can I delete my account?**"):
                        st.write("To delete your existing account, please contact the Commission at cosoa@iskolarngbayan.pup.edu.ph.")
                        
                elif faq_type == "Contact Us":
                    with st.expander("**How can I contact the Office of Student Services (OSS)?**"):
                        st.write("You can contact the OSS through the following channels:")
                        st.write("- **Email:** studentservices@pup.edu.ph")
                    with st.expander("**How can I provide feedback or suggestions?**"):
                        st.write("To report a technical issue, please contact the Commission through the following:")
                        st.write("- **Official webmail:** cosoa@iskolarngbayan.pup.edu.ph.")
                        st.write("- **Official Facebook page:** https://www.facebook.com/pup.sccosoa")

                elif faq_type == "Fundraising":
                    with st.expander("**Can we organize fundraising activities now? What are the guidelines for these?**"):
                        st.write("Yes, as per Executive Order No. 12, Series of 2024, the University President issued the regulation of fund-raising activities and collection activities to all accredited student organizations. You may view the Revised Guidelines and Required Documents through this hyperlink. https://bit.ly/ExecutiveOrder12Series2024")
                    with st.expander("**What are the required documents that we must submit to collect membership fees?**"):
                        st.write("Kindly consult with the Office of Student Services (OSS) to ensure updated guidelines and requirements for collecting membership fees.")
                    with st.expander("**What is the maximum amount that we could collect for the membership fee?**"):
                        st.write("According to Title 7, Section 13.3 of the 2019 PUP Student handbook, an organization's membership fee shall not be more than Fifty Pesos (Php 50.00) per semester.")
                    with st.expander("**Are we allowed to collect membership fees?**"):
                        st.write("Yes.")
                    with st.expander("**If we want our organization to have shirts and/or lanyards, do we still have to process documents, and what are those? Is it counted as a fundraising activity?**"):
                        st.write("If there is no profit, it is not counted as a fundraising activity. There are no documents needed, however, please consult with PUP SC COA regarding the organization’s Financial Statements.")
                elif faq_type == "General":
                    with st.expander("**How long do we have to wait until we receive an email regarding the documents we have submitted?**"):
                        st.write("All lapses found in the documents will be sent through an email within twelve (12) calendar days from the next Monday it was submitted.")
                    with st.expander("**Shall we wait for the email from PUP SC COSOA containing notes regarding our previous submission before submitting another set of documents?**"):
                        st.write("Yes.")
                    with st.expander("**After correcting our previous lapses and resubmitting our documents, is there an assurance that our organization’s documents don’t have lapses and are already subjected to accreditation/revalidation approval?**"):
                        st.write("The Office of the Chairperson will release a memorandum stating the organizations that passed the COSOA Chairperson’s Approval and will be endorsed to the Office of Student Services (OSS).")
                    with st.expander("**Is it required to put our organization’s letterhead on our documents?**"):
                        st.write("No, it is optional. However, keep in mind that if the letterhead of a document is from the Commission, you are prohibited from removing or editing it.")
                    with st.expander("**Is it fine if we do not put any attachments on our Accomplishment Report?**"):
                        st.write("Attachments (e.g., list of attendees, members, etc.) are not required, but you should put at least three (3) pieces of documentation (e.g., screenshots, event receipts, etc.)")
                    with st.expander("**Are there any documents we can submit as an alternative to the Certificate of Registration that don’t have a QR code?**"):
                        st.write("You may submit either your PUPSIS-generated First Semester confirmation slip, Certificate of Enrollment, or class schedule.")
                    with st.expander("**Are we allowed to put “SGD” for the signatories’ part instead of our e-signatures?**"):
                        st.write("No, all documents must be signed.")
                    with st.expander("**For the Accomplishment Report, if the officer with the highest rank (e.g., President) was the one who prepared this document, whom shall we put on the signatory of approval?**"):
                        st.write("The next highest-ranking officer.")
                    with st.expander("**For the General Plan of Activities (GPOA), under the month column, should we include the year (e.g., December 2022) based on the given accomplished templates?**"):
                        st.write("Yes.")
                    with st.expander("**What are the guidelines for conducting on-site activities/programs?**"):
                        st.write("Kindly contact us at our webmail (cosoa@iskolarngbayan.pup.edu.ph) or at our official Facebook page (link here) for more information.")
                elif faq_type == "COA":
                    with st.expander("**When is the deadline for submitting accreditation and revalidation applications?**"):
                        st.write("The initial deadline is October 21, 2024, and the process may take up to 15 working days, depending on the accuracy of the submitted documents.")
                    with st.expander("**What are the financial statement recording periods?**"):
                        st.write("Financial statements should cover the period from September 25, 2023, to September 9, 2024. Any turnovers after September 9, 2024, should have the turnover date as the ending date of the financial statement.")
                    with st.expander("**What happens if I submit incomplete or inaccurate documents?**"):
                        st.write("If lapses are found, the Commission will notify the organization through an audit report. The organization has up to three (3) chances to resubmit corrected documents. Failure to rectify the issues will result in the Commission not forwarding the application to the OSS.")
                    with st.expander("**Can I appeal if my organization exceeds the three resubmission chances?**"):
                        st.write("Yes, an appeal can be sent to the PUP SC COA. However, it will only be entertained if an extension to the deadline is granted.")
                    with st.expander("**What type of receipts and documents are accepted as evidence?**"):
                        st.write("The Commission will accept electronic receipts as source documents. If no official receipt is available, an acknowledgment receipt or letter is also acceptable.")
                    with st.expander("**Can I submit an official receipt instead of an acknowledgment receipt?**"):
                        st.write("Yes, official receipts are accepted as proof of expenses. However, if official receipts are unavailable, acknowledgment receipts must meet the required percentages (90% for expenses exceeding ₱10,000 and 70% for expenses below ₱10,000).")
                    with st.expander("**What happens if my submission lacks the required percentage of acknowledgment receipts?**"):
                        st.write("If the submission does not meet the required percentages, the Commission may request additional documentation or clarification, and your organization may need to resubmit the necessary receipts to complete the process.")
                    with st.expander("**How can I claim my approved Financial Clearance?**"):
                        st.write("The approved Financial Clearance must be claimed from the OSS, and it is the organization's responsibility to submit it to PUP SC COSOA.")
                    with st.expander("**What if we don't have a new set of officers yet?**"):
                        st.write("The Commission cannot grant the auditing unless the turnover of assets has been done for the AY. 24-25.")

if __name__ == "__main__":
    faqs()