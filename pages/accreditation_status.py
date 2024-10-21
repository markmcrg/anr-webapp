import streamlit as st
import streamlit_antd_components as sac
from datetime import datetime
# Add the main directory to the system path if necessary
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers import authenticate_b2, get_submissions


def accreditation_status():
    if 'bucket' not in st.session_state:
        st.session_state.bucket = authenticate_b2('anr-webapp')
    bucket = st.session_state.bucket
    download_auth_token = bucket.get_download_authorization("", 86400)
    # API call to fetch user's submissions based on username
    data = get_submissions(st.session_state.username)
    if data:
        st.markdown("<h1 style='color: #f5c472; text-align:left; padding-bottom:60px;'>My Submissions</h1>", unsafe_allow_html=True)
        # Create table rows dynamically
        rows = ""
        for item in data:
            if item['eval_phase'] == "IE":
                eval_phase = "Initial Evaluation"
                status_class = "status-evaluation"
                status_icon = "bi-hourglass-split"
            elif item['eval_phase'] == "FE":
                eval_phase = "Final Evaluation"
                status_class = "status-evaluation"
                status_icon = "bi-hourglass-split"
            elif item['eval_phase'] == "CA":
                eval_phase = "Chairperson's Approval"
                status_class = "status-evaluation"
                status_icon = "bi-hourglass-split"
            elif item['eval_phase'] == "Returned":
                eval_phase = "Returned for Revisions"
                status_class = "status-returned"
                status_icon = "bi-arrow-counterclockwise"
            elif item['eval_phase'] == "Approved":
                eval_phase = "Approved"
                status_class = "status-approved"
                status_icon = "bi-check-circle-fill"
            elif item['eval_phase'] == 'Rejected':
                eval_phase = "Rejected"
                status_class = "status-returned"
                status_icon = "bi-x-circle-fill"
            
            b2_file_url = f"{item['b2_file_url']}?Authorization={download_auth_token}"
            date_submitted = datetime.strptime(item['date_submitted'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            last_updated = datetime.strptime(item['last_updated'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
               
            rows += f"""
            <tr>
                <td class="text-left">{item["org_name"]}</td>
                <td>{item["jurisdiction"]}</td>
                <td>{item["app_type"]}</td>
                <td>{item["app_order"]}</td>
                <td>{date_submitted}</td>
                <td>{last_updated}</td>
                <td><span class="{status_class}"><i class="bi {status_icon}"></i> {eval_phase}</span></td>
                <td><a href="{b2_file_url}" class="btn btn-sm btn-outline-maroon">View</a></td>
            </tr>
            """
            
        table_html = f"""
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style>
                h1 {{
                    font-family: "Source Sans Pro", sans-serif;
                    font-weight: 700;
                    color: rgb(49, 51, 63);
                    padding: 1.25rem 0px 1rem;
                    margin: 0px;
                    line-height: 1.2;
                }}
                .table {{
                    border-radius: 15px;
                    overflow: hidden;
                    margin-bottom: 0;
                    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                }}
                .table thead {{
                    background-color: #800000;
                    color: white;
                }}
                .table th, .table td {{
                    vertical-align: middle;
                    text-align: center;
                }}
                .table th {{
                    text-transform: capitalize;
                }}
                .status-approved {{
                    color: #28a745;
                }}
                .status-evaluation {{
                    color: #ffc107;
                }}
                .status-returned {{
                    color: #dc3545;
                }}
                .table td {{
                    background-color: white !important;
                }}
                .text-left {{
                    text-align: left !important;
                }}
                .btn-outline-maroon {{
                    color: maroon !important;
                    border-color: maroon !important; 
                }}
                .btn-outline-maroon:hover {{
                    background-color: maroon !important;
                    color: white !important;
                }}
            </style>

            <table class="table table-hover">
                <thead>
                    <tr>
                        <th class="text-left">Organization Name</th>
                        <th>Jurisdiction</th>
                        <th>Application Type</th>
                        <th>Application Order</th>
                        <th>Date Submitted</th>
                        <th>Last Updated</th>
                        <th>Status</th>
                        <th>View</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
            </table>
        """
        st.markdown(table_html, unsafe_allow_html=True)
        
        # Check each submission if existing, if not then disable the respective option
        # Add chairperson's remarks to the tracker form at the bottom
        
        # Checking for entries
        app_orders = {"Initial Submission": False, "1st Resubmission": False,  "2nd Resubmission": False}

        # Iterate through the data and check for specific 'app_order' values
        for entry in data:
            if entry["app_order"] in app_orders:
                app_orders[entry["app_order"]] = True
        cols = st.columns([0.2, 0.8], vertical_alignment='top')
        with cols[0]:
            # with st.container(border=True):
                sub_to_view = sac.segmented(
                                    items=[
                                        sac.SegmentedItem(label='Initial Submission', disabled=not app_orders["Initial Submission"]),
                                        sac.SegmentedItem(label='1st Resubmission', disabled=not app_orders["1st Resubmission"]),
                                        sac.SegmentedItem(label='2nd Resubmission', disabled=not app_orders["2nd Resubmission"]),
                                    ], direction='vertical', align='center', key='sub_view'
                )
        with cols[1]:
            with st.container(border=True):
                selected_record = next((entry for entry in data if entry["app_order"] == sub_to_view))
                
                # Check if status is returned first, then check application type (accre or reval)
                if selected_record['eval_phase'] == 'Returned':
                    tracker_form_data = ""
                    accre_docs = {
                        'AD001': 'Compilation of Compulsory Certificates',
                        'AD002': 'Officers’ Profile with 1st Semester COR',
                        'AD003': 'Adviser(s)’s Letter of Concurrence',
                        'AD004': 'Student Organization’s Constitution and Bylaws (CBL)',
                        'AD005': 'General Plan of Activities with Budgetary Outlay',
                    }
                    reval_docs = {
                        'RD001': 'Compilation of Compulsory Certificates',
                        'RD002': 'Officers’ Profile with 1st Semester COR',
                        'RD003': 'Adviser(s)’s Letter of Concurrence',
                        'RD004': 'Student Organization’s Constitution and Bylaws (CBL)',
                        'RD005': 'General Plan of Activities with Budgetary Outlay',
                        'RD006': 'Accomplishment Report',
                        'RD007': 'Copy of Approved Financial Statements',
                        'RD008': 'Turnover of Assets and Funds',
                    }
                    if selected_record['app_type'] == 'Accreditation':
                        accre_doc_names = [doc_name for doc_name in accre_docs.values()]
                        for idx, doc_name in enumerate(accre_doc_names, start=1):
                            if selected_record[f'REQ{idx:03d}_approved'] == '1':
                                status_icon = 'check'
                                status_class = 'status-check'
                            else:
                                status_icon = 'times'
                                status_class = 'status-cross'
                            tracker_form_data += f"""
                            <tr>
                                <td class="center-align">AD{idx:03d}</td>
                                <td class="left-align">{doc_name}</td>
                                <td class="center-align"><i class="fas fa-{status_icon} status-icon {status_class}"></i></td>
                                <td class="left-align">{selected_record[f'REQ{idx:03d}_remarks']}</td>
                            </tr>
                            """            
                    elif selected_record['app_type'] == 'Revalidation':
                        reval_doc_names = [doc_name for doc_name in reval_docs.values()]    
                        for idx, doc_name in enumerate(reval_doc_names, start=1):
                            if selected_record[f'REQ{idx:03d}_approved'] == '1':
                                status_icon = 'check'
                                status_class = 'status-check'
                            else:
                                status_icon = 'times'
                                status_class = 'status-cross'
                            tracker_form_data += f"""
                            <tr>
                                <td class="center-align">RD{idx:03d}</td>
                                <td class="left-align">{doc_name}</td>
                                <td class="center-align"><i class="fas fa-{status_icon} status-icon {status_class}"></i></td>
                                <td class="left-align">{selected_record[f'REQ{idx:03d}_remarks']}</td>
                            </tr>
                            """   
                    st.markdown(f"""
                                        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
                                        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css" rel="stylesheet">
                                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                                        <style>
                                            body {{
                                                font-family: Arial, sans-serif;
                                                display: flex;
                                                justify-content: center;
                                                align-items: center;
                                                min-height: 100vh;
                                                margin: 0;
                                                background-color: #f0f0f0;
                                            }}
                                            table {{
                                                border-collapse: separate;
                                                border-spacing: 0;
                                                border-radius: 10px;
                                                overflow: hidden;
                                                box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                                                background-color: #ffffff;
                                                width:100%;
                                            }}
                                            th, td {{
                                                padding: 12px 15px;
                                                border-bottom: 1px solid #e0e0e0;
                                            }}
                                            th {{
                                                background-color: #800000;
                                                color: white;
                                            }}
                                            tr:last-child td {{
                                                border-bottom: none;
                                            }}
                                            tr:nth-child(even) {{
                                                background-color: #f8f8f8;
                                            }}
                                            .status-icon {{
                                                font-size: 1.2em;
                                            }}
                                            .status-check {{
                                                color: #28a745;
                                            }}
                                            .status-cross {{
                                                color: #dc3545;
                                            }}
                                            .center-align {{
                                                text-align: center;
                                            }}
                                            .left-align {{
                                                text-align: left;
                                            }}
                                        </style>
                                        <table>
                                            <tr>
                                                <th colspan="4" class="center-align">{selected_record['filename']}</th>
                                            </tr>
                                            <tr>
                                                <th class="center-align">Code</th>
                                                <th class="left-align">Form Name</th>
                                                <th class="center-align">Status</th>
                                                <th class="center-align">Remarks</th>
                                            </tr>
                                        {tracker_form_data}
                                            
                                        """, unsafe_allow_html=True)
                    # sac.alert(label='Chairperson\'s Remarks: Please check your...', size='sm', variant='quote-light', color='info', icon=True)
            
                else:
                    sac.result(label='Tracker Form Unavailable.', description='Please wait until your submission is tagged as "Returned."')

    else:
        cols=st.columns([0.5, 1, 0.5])
        with cols[1]:
            st.markdown("<h1 style='color: #f5c472; text-align:left; margin-left: 10px;'>My Submissions</h1>", unsafe_allow_html=True)
            with st.container(border=True):
                sac.result(label='No Submissions Found', description='Click on "Accreditation Application" to submit your first application.', status='empty')
    

# Have info to show what each status means (Approved, Pending, etc.)
# Tracker form should only be visible once returned for revisions is the eval phase