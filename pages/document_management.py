import streamlit as st
from dts import DTS
import os
import hydralit_components as hc
def document_management():
    cols = st.columns([0.25, 1, 0.25])

    with cols[1]:
        with st.container(border=True):
            st.subheader("📄 View Document Status")
            with st.form(key='my_form'):
                dts_num = st.text_input(label='**Enter DTS Number**', placeholder="DTS Number (e.g. DT2024XXXXXX)", max_chars=12)
                # Check if the length of the input is exactly 12 characters
                submit_button = st.form_submit_button(label='Trace')
                dts_num = dts_num.upper()
                
            placeholder = st.empty() # Remove re-rendering of the form
            if submit_button and not dts_num.startswith('DT202'):
                st.error("Invalid DTS Number. Please enter a valid DTS Number starting with DT + the current year (e.g., DT2024XXXXXX)")
            elif submit_button and len(dts_num) != 12:
                st.error("Invalid DTS Number. Please enter a valid DTS Number with 12 characters.")   
            elif submit_button and dts_num.startswith('DT202'):
                email = os.environ['dts_email']
                pw = os.environ['dts_pass']
                with hc.HyLoader('',hc.Loaders.standard_loaders,index=[2]):
                    doc = DTS(email=email, password=pw)
                    
                
                    result = doc.track(dts_num)
                    details = result.get("details", {})
                    items = result.get("action_items", [])
                    if not details:
                        st.error("No document found with the given DTS Number.")
                        return

                    st.header(f"🔔 {dts_num}")

                    # Display document details
                    with st.container(border=True):
                        st.subheader("📄 Document Details")
                        for key, value in details.items():
                            st.write(f"**{key}:** {value}")

                    st.write("---")

                    # Display document thread
                    st.subheader("📝 Document Thread")
                    st.markdown("*Sorted from latest to oldest*")
                    for item in items:
                        with st.container(border=True):
                            # Date and time of the action
                            st.write(f"**{item['date_time']}**")

                            # Office and staff involved
                            st.write(f"**{item['office_staff']}**")

                            # Action taken
                            st.write(f"**Action:** {item['date_time']}")

                            # Comments (if any)
                            if item['detail_text'] != "":
                                st.write(f"**Comments:** {item['detail_text']}")
