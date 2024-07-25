import streamlit as st
import streamlit_antd_components as sac
import pandas as pd

st.set_page_config(page_title="Application Requirements", page_icon="📋", layout="wide")

st.markdown("<h1 style='text-align: center;'>Application Requirements</h1>", unsafe_allow_html=True)

cols = st.columns([0.4,1,0.4])


with cols[1]:
    accre_type = sac.segmented(
        items=[
            sac.SegmentedItem(label='Accreditation'),
            sac.SegmentedItem(label='Revalidation'),
        ],  align='center', radius='xl', divider=True, use_container_width=True,
    )

if accre_type == "Accreditation":
    columns = ["Form Code", "Requirement", "Template", "Sample"]
    table_data = [
        ["AD001", "Certificate of Recognition from Central/Local Student Council", "Download", "View"],
        ["AD002", "Official List of Officers and Adviser(s) with signatures over printed names, and list of members (at least 15 members including the officers/executives)", "Download", "View"],
        ["AD003", "Officers’ Profile with 1st Semester Certificate of Registration", "Download", "View"],
        ["AD004", "Adviser(s)’s Letter of Concurrence with scanned copy of their university-issued ID", "Download", "View"],
        ["AD005", "Student Organization’s Constitution and Bylaws (CBL)", "Download", "View"],
        ["AD006", "General Plan of Activities with Budgetary Outlay", "Download", "View"],
        ["AD007", "Organization's Advocacy Plan", "Download", "View"],
        ["AD008", "Certificate of Clearance from PUP Student Council Commission on Audit (PUP SC COA)", "Download", "View"],
        ["AD009", "OSS Anti-Hazing Orientation Certificate of Registration", "Download", "View"],
    ]
    
    # Convert the data to a DataFrame
    accre_reqs_df = pd.DataFrame(table_data, columns=columns)
    accre_reqs_df = accre_reqs_df.style.hide(axis="index").set_table_styles([{
        'selector': '.col2, .col3',  
        'props': [
            ('text-align', 'center')
        ]
    }])
    st.markdown(f"<div style='max-width: fit-content; margin-inline: auto;'>{accre_reqs_df.to_html(index=False)}</div>", unsafe_allow_html=True)

    
elif accre_type == "Revalidation":
    columns = ["Form Code", "Requirement", "Template", "Sample"]
    table_data = [
        ["RD001", "Certificate of Recognition from Central/Local Student Council", "Download", "View"],\
        ["RD002", "Scanned Copy of the Latest Certificate of Accreditation/Revalidation", "Download", "View"],
        ["RD003", "Official List of Officers and Adviser(s) with signatures over printed names, and list of members (at least 15 members including the officers/executives)", "Download", "View"],
        ["RD004", "Officers’ Profile with 1st Semester Certificate of Registration", "Download", "View"],
        ["RD005", "Adviser(s)’s Letter of Concurrence with scanned copy of their university-issued ID", "Download", "View"],
        ["RD006", "Student Organization’s Constitution and Bylaws (CBL)", "Download", "View"],
        ["RD007", "General Plan of Activities with Budgetary Outlay", "Download", "View"],
        ["RD008", "Organization's Advocacy Plan", "Download", "View"],
        ["RD009", "Accomplishment Report", "Download", "View"],
        ["RD09X", "Accomplishment Report Substitute", "Download", "View"],
        ["RD010", "Financial Statements", "Download", "View"],
        ["RD011", "Certificate of Clearance from PUP Student Council Commission on Audit (PUP SC COA)", "Download", "View"],
        ["RD012", "Turnover of Assets and Funds", "Download", "View"],
        ["RD013", "OSS Anti-Hazing Orientation Certificate of Registration", "Download", "View"],
    ]
    
    reval_reqs_df = pd.DataFrame(table_data, columns=columns)
    reval_reqs_df = reval_reqs_df.style.hide(axis="index").set_table_styles([{
        'selector': '.col2, .col3',  
        'props': [
            ('text-align', 'center')
        ]
    }])
    st.markdown(f"<div style='max-width: fit-content; margin-inline: auto;'>{reval_reqs_df.to_html(index=False)}</div>", unsafe_allow_html=True)
    