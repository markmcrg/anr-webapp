import streamlit as st
from helpers import authenticate_b2, get_submissions
import streamlit_antd_components as sac
from datetime import datetime

def accreditation_status():
    # session state this bucket to minimize API calls
    bucket = authenticate_b2('anr-webapp')
    download_auth_token = bucket.get_download_authorization("", 86400)
    st.subheader("My Submissions")
    # API call to fetch user's submissions based on username
    data = get_submissions(st.session_state["username"])
    if data:
        # Create table rows dynamically
        rows = ""
        for item in data:
            if item['eval_phase'] == "IE1":
                eval_phase = "Initial Evaluation 1"
                status_class = "status-evaluation"
                status_icon = "bi-hourglass-split"
            elif item['eval_phase'] == "IE2":
                eval_phase = "Initial Evaluation 2"
                status_class = "status-evaluation"
                status_icon = "bi-hourglass-split"
            elif item['eval_phase'] == "FE1":
                eval_phase = "Final Evaluation 1"
                status_class = "status-evaluation"
                status_icon = "bi-hourglass-split"
            elif item['eval_phase'] == "FE2":
                eval_phase = "Final Evaluation 2"
                status_class = "status-evaluation"
                status_icon = "bi-hourglass-split"
                
            elif item['eval_phase'] == "returned":
                eval_phase = "Returned for Revisions"
                status_class = "status-returned"
                status_icon = "bi-arrow-counterclockwise"
            elif item['eval_phase'] == "approved":
                eval_phase = "Approved"
                status_class = "status-approved"
                status_icon = "bi-check-circle-fill"
            
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
            <style>
                .table {{
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10px;
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
                .text-left {{
                    text-align: left !important;
                }}
                .btn-outline-maroon {{
                    color: maroon !important;
                    border-color: maroon;
                }}
                .btn-outline-maroon:hover {{
                    background-color: maroon;
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
    else:
        sac.result(label='No Submissions Found', description='Click on "Accreditation Application" to submit your first application.', status='empty')
    

# Have info to show what each status means (Approved, Pending, etc.)