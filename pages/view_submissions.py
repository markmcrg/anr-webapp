import streamlit as st

# # Add the main directory to the system path if necessary
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helpers import (
    fetch_data,
    submit_evaluation_accre,
    submit_evaluation_reval,
    modify_eval_phase,
    send_notif_email,
    get_email,
    get_abbreviation,
    authenticate_b2,
    get_role,
    update_last_updated,
    add_chair_remarks
)
import pandas as pd
from st_keyup import st_keyup
import time
import streamlit_antd_components as sac

if "disable_save_btn" not in st.session_state:
    st.session_state["disable_save_btn"] = False
if "disable_selectbox" not in st.session_state:
    st.session_state["disable_selectbox"] = False
    

def disable_save_btn_and_selectbox():
    st.session_state["disable_save_btn"] = True
    st.session_state["disable_selectbox"] = True
    
def discard_changes():
    st.session_state["disable_save_btn"] = False
    st.session_state["disable_selectbox"] = False
    st.session_state["show_eval_summary"] = False
    
def evaluate_another_org():
    st.session_state["disable_save_btn"] = False
    st.session_state["disable_selectbox"] = False
    
def view_submissions():
    with st.container(border=True):
        st.subheader("📋 Evaluate Submissions")

        submission_data = fetch_data(
            "https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_all_submissions"
        )["data"]["rows"]
        submission_data_df = pd.DataFrame(submission_data)
        submission_data_df = submission_data_df.rename(
            columns={
                "filename": "Organization Submission",
                "jurisdiction": "Jurisdiction",
                "app_type": "Application Type",
                "date_submitted": "Date Submitted",
                "eval_phase": "Evaluation Phase",
                "b2_file_url": "View",
            }
        )

        submission_data_df["Date Submitted"] = pd.to_datetime(
            submission_data_df["Date Submitted"]
        )

        top_cols = st.columns([0.75, 0.625, 0.5], vertical_alignment="center")
        with top_cols[0]:
            submission_query = st_keyup(
                "Search for an organization or user:",
                debounce=300,
                key="1",
                placeholder="Organization Name/Abbreviation or Person Assigned",
            )
        with top_cols[1]:
            # CHANGE THIS BACK AFTER TESTING
            # role = get_role(st.session_state["username"])
            role = 'chair'

            if role in ["enbanc", "chair"]:
                eval_phase_filter = st.pills(
                    "**Select evaluation phases to view:**",
                    ["IE", "FE", "CA", "Returned", "Approved", "Rejected"],
                    key="5",
                    selection_mode="multi",
                    default=["IE", "FE", "CA"],
                )

            elif role == "cosoa":
                eval_phase_filter = st.pills(
                    "**Select evaluation phases to view:**",
                    ["IE", "FE", "Returned"],
                    key="5",
                    selection_mode="multi",
                    default=["IE"],
                )
            if eval_phase_filter:
                submission_data_df = submission_data_df[
                    submission_data_df["Evaluation Phase"].isin(eval_phase_filter)
                ]
            else:
                submission_data_df = pd.DataFrame()
            with top_cols[2]:
                sort_filter = st.selectbox(
                    "**Sort by:**",
                    [
                        "Date Submitted (Ascending)",
                        "Date Submitted (Descending)",
                        "Evaluation Phase (Ascending)",
                        "Evaluation Phase (Descending)",
                    ],
                    key="3",
                )
                if sort_filter == "Date Submitted (Ascending)":
                    submission_data_df = submission_data_df.sort_values(
                        by="Date Submitted", ascending=True
                    )
                elif sort_filter == "Date Submitted (Descending)":
                    submission_data_df = submission_data_df.sort_values(
                        by="Date Submitted", ascending=False
                    )
                elif sort_filter == "Evaluation Phase (Ascending)":
                    submission_data_df = submission_data_df.sort_values(
                        by="Evaluation Phase", ascending=False
                    )
                elif sort_filter == "Evaluation Phase (Descending)":
                    submission_data_df = submission_data_df.sort_values(
                        by="Evaluation Phase", ascending=True
                    )
            if submission_query:
                submission_data_df = submission_data_df[
                    submission_data_df["Organization Submission"].str.contains(
                        submission_query, case=False, regex=False
                    )
                ]

        table_data = ""
        if not submission_data_df.empty:
            bucket = authenticate_b2("anr-webapp")
            download_auth_token = bucket.get_download_authorization("", 86400)
            for idx, row in submission_data_df.iterrows():
                if row["Evaluation Phase"] == "IE":
                    eval_phase = "Initial Evaluation"
                    status_class = "status-initial-evaluation"
                    status_icon = "bi-hourglass-split"
                elif row["Evaluation Phase"] == "FE":
                    eval_phase = "Final Evaluation"
                    status_class = "status-evaluation"
                    status_icon = "bi-hourglass-split"
                elif row["Evaluation Phase"] == "CA":
                    eval_phase = "Chairperson's Approval"
                    status_class = "status-ca"
                    status_icon = "bi-hourglass-split"
                elif row["Evaluation Phase"] == "Returned":
                    eval_phase = "Returned for Revisions"
                    status_class = "status-returned"
                    status_icon = "bi-arrow-counterclockwise"
                elif row["Evaluation Phase"] == "Approved":
                    eval_phase = "Approved"
                    status_class = "status-approved"
                    status_icon = "bi-check-circle-fill"
                elif row["Evaluation Phase"] == "Rejected":
                    eval_phase = "Rejected"
                    status_class = "status-returned"
                    status_icon = "bi-x-circle-fill"
                date_submitted = row["Date Submitted"].strftime("%Y-%m-%d")

                b2_file_url = f"{row['View']}?Authorization={download_auth_token}"

                table_data += f"""
                <tr>
                    <td class="center-align">{row['Organization Submission']}</td>
                    <td class="center-align">{row['Jurisdiction']}</td>
                    <td class="center-align">{row['Application Type']}</td>
                    <td class="center-align">{date_submitted}</td>
                    <td class="center-align"><span class="{status_class}"><i class="bi {status_icon}"></i> {eval_phase}</span></td>
                    <td class="center-align"><a href="{b2_file_url}" class="btn btn-sm btn-outline-maroon">View</a></td>
                </tr>
                """
        st.markdown(
            f"""                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
                                        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css" rel="stylesheet">
                                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                                        <style>
                                            .st-key-5 {{
                                                padding-left:40px;
                                            }}
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
                                                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                                                background-color: #ffffff;
                                                width:100%;
                                            }}
                                            th, td {{
                                                padding: 5px 8px !important;
                                            }}
                                            th {{
                                                background-color: #800000;
                                                color: white;
                                            }}
                                            th {{
                                                font-size: 16px !important;
                                            }}
                                            td {{
                                                font-size: 15px !important;
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
                                            .status-approved {{
                                                color: #28a745;
                                            }}
                                            .status-ca {{
                                                color: #0379ff;
                                            }}
                                            .status-evaluation {{
                                                color: #6610f2;
                                            }}
                                            .status-initial-evaluation {{
                                                color: #fcad03;
                                            }}
                                            .status-returned {{
                                                color: #dc3545;
                                            }}
                                            .center-align {{
                                                text-align: center;
                                            }}
                                            .left-align {{
                                                text-align: left;
                                            }}
                                            .btn-outline-maroon {{
                                                color: maroon !important;
                                                border-color: maroon !important;
                                            }}
                                            .btn-outline-maroon:hover {{
                                                background-color: maroon !important;
                                                color: white !important
                                            }}
                                            .date-padding{{
                                                padding: 6px 30px !important;
                                            }}
                                        </style>
                                        <table>
                                            <tr>
                                                <th class="center-align">Organization Submission</th>
                                                <th class="left-align">Jurisdiction</th>
                                                <th class="center-align">Type</th>
                                                <th class="center-align date-padding">Date</th>
                                                <th class="center-align">Evaluation Phase</th>
                                                <th class="center-align">View</th>
                                            </tr>
                                            {table_data}
                                            
                                            
                                        """,
            unsafe_allow_html=True,
        )  # noqa: F541

        eval_data = {}
        accre_docs = {
            "AD001": "Compilation of Compulsory Certificates",
            "AD002": "Officers’ Profile with 1st Semester COR",
            "AD003": "Adviser(s)’s Letter of Concurrence",
            "AD004": "Student Organization’s Constitution and Bylaws (CBL)",
            "AD005": "General Plan of Activities with Budgetary Outlay",
        }
        reval_docs = {
            "RD001": "Compilation of Compulsory Certificates",
            "RD002": "Officers’ Profile with 1st Semester COR",
            "RD003": "Adviser(s)’s Letter of Concurrence",
            "RD004": "Student Organization’s Constitution and Bylaws (CBL)",
            "RD005": "General Plan of Activities with Budgetary Outlay",
            "RD006": "Accomplishment Report",
            "RD007": "Copy of Approved Financial Statements",
            "RD008": "Turnover of Assets and Funds",
        }

        def display_previous_remarks(data, doc_code, idx):
            with st.popover("View Previous Remarks"):
                prev_remark = data[f"REQ{idx:03d}"]["remarks"]
                st.write(
                    "\n".join(
                        line if line.strip().startswith("- ") else f"- {line.strip()}"
                        for line in prev_remark.split("\n")
                        if line.strip()
                    )
                )

        def show_expander(documents, data=None):
            for idx, (doc_code, doc_name) in enumerate(documents.items(), start=1):
                with st.expander(f"{doc_code} - {doc_name}"):
                    if data:
                        display_previous_remarks(data, doc_code, idx)
                    remark = st.text_area(
                        f"Remarks for {doc_name}", key=f"remark_{doc_code}", height=100
                    )
                    approved = st.checkbox(
                        f"Approve {doc_code}", key=f"approve_{doc_code}"
                    )
                    eval_data[doc_code] = {"approved": approved, "remark": remark}

        def show_expander_returned(documents, data):
            for idx, (doc_code, doc_name) in enumerate(documents.items(), start=1):
                with st.expander(f"{doc_code} - {doc_name}"):
                    prev_remark = data[f"REQ{idx:03d}"]["remarks"]
                    st.write(
                        "\n".join(
                            line
                            if line.strip().startswith("- ")
                            else f"- {line.strip()}"
                            for line in prev_remark.split("\n")
                            if line.strip()
                        )
                    )

        def get_filtered_record(submission_data_df, sub_to_eval, exclude_phase="IE"):
            return submission_data_df[
                (submission_data_df["Evaluation Phase"] != exclude_phase)
                & (submission_data_df["Organization Submission"] == sub_to_eval)
            ]

        def extract_data(filtered_record, num_requirements):
            data = {}
            if not filtered_record.empty:
                for i in range(1, num_requirements + 1):
                    req_key = f"REQ{i:03d}"
                    data[req_key] = {
                        "approved": filtered_record[f"{req_key}_approved"].values[0],
                        "remarks": filtered_record[f"{req_key}_remarks"].values[0],
                    }
            return data

        if not submission_data_df.empty:
            st.write("---")
            cols = st.columns([1, 1], gap="medium")
            with cols[0]:
                sub_to_eval = st.selectbox(
                    "**Select submission to evaluate:**",
                    submission_data_df["Organization Submission"],
                    index=None,
                    disabled=st.session_state["disable_selectbox"],
                )
                if sub_to_eval:
                    username = submission_data_df[
                        submission_data_df["Organization Submission"] == sub_to_eval
                    ]["username"].item()

                    app_order = submission_data_df[
                        submission_data_df["Organization Submission"] == sub_to_eval
                    ]["app_order"].item()

                    eval_phase = submission_data_df[
                        submission_data_df["Organization Submission"] == sub_to_eval
                    ]["Evaluation Phase"].item()

                    app_type = submission_data_df[
                        submission_data_df["Organization Submission"] == sub_to_eval
                    ]["Application Type"].item()

                    with st.form("evaluation_form", border=False):
                        if eval_phase == "IE":
                            if app_type == "Accreditation":
                                show_expander(accre_docs)
                            elif app_type == "Revalidation":
                                show_expander(reval_docs)

                        elif eval_phase in ["FE", "CA"]:
                            filtered_record = get_filtered_record(
                                submission_data_df, sub_to_eval
                            )
                            num_requirements = 5 if app_type == "Accreditation" else 8
                            data = extract_data(filtered_record, num_requirements)

                            if app_type == "Accreditation":
                                show_expander(accre_docs, data)
                            elif app_type == "Revalidation":
                                show_expander(reval_docs, data)
                        elif eval_phase == "Returned":
                            sac.alert(
                                label="This submission has been returned for revisions.",
                                size="sm",
                                variant="quote-light",
                                color="info",
                                icon=True,
                            )
                            filtered_record = get_filtered_record(
                                submission_data_df, sub_to_eval
                            )
                            num_requirements = 5 if app_type == "Accreditation" else 8
                            data = extract_data(filtered_record, num_requirements)
                            if app_type == "Accreditation":
                                show_expander_returned(accre_docs, data)
                            elif app_type == "Revalidation":
                                show_expander_returned(reval_docs, data)

                        save_btn = st.form_submit_button("Save", on_click=disable_save_btn_and_selectbox, disabled=st.session_state["disable_save_btn"])
                    if st.session_state["disable_save_btn"] and st.session_state['disable_selectbox']:
                        st.button("Discard Changes", on_click=discard_changes)

                            

                    if "show_eval_summary" not in st.session_state:
                        st.session_state["show_eval_summary"] = False

                    if st.session_state["show_eval_summary"] is False:
                        with cols[1]:
                            tracker_form_data = ""
                            filename = submission_data_df[
                                submission_data_df["Organization Submission"]
                                == sub_to_eval
                            ]["Organization Submission"].item()
                            tracker_form = st.empty()
                            if eval_phase == "IE":
                                if app_type == "Accreditation":
                                    accre_doc_names = [
                                        doc_name for doc_name in accre_docs.values()
                                    ]
                                    for idx, doc_name in enumerate(
                                        accre_doc_names, start=1
                                    ):
                                        tracker_form_data += f"""
                                        <tr>
                                            <td class="center-align">AD{idx:03d}</td>
                                            <td class="left-align">{doc_name}</td>
                                            <td class="center-align"><i class="fas fa-times status-icon status-cross"></i></td>
                                        </tr>
                                        """
                                elif app_type == "Revalidation":
                                    with tracker_form.container():
                                        reval_doc_names = [
                                            doc_name for doc_name in reval_docs.values()
                                        ]
                                        for idx, doc_name in enumerate(
                                            reval_doc_names, start=1
                                        ):
                                            tracker_form_data += f"""
                                            <tr>
                                                <td class="center-align">RD{idx:03d}</td>
                                                <td class="left-align">{doc_name}</td>
                                                <td class="center-align"><i class="fas fa-times status-icon status-cross"></i></td>
                                            """
                            if eval_phase in [
                                "FE",
                                "CA",
                                "Returned",
                                "Approved",
                                "Rejected",
                            ]:
                                if app_type == "Accreditation":
                                    accre_doc_names = [
                                        doc_name for doc_name in accre_docs.values()
                                    ]
                                    for idx, doc_name in enumerate(
                                        accre_doc_names, start=1
                                    ):
                                        if data[f"REQ{idx:03d}"]["approved"] == "1":
                                            status_icon = "check"
                                            status_class = "status-check"
                                        else:
                                            status_icon = "times"
                                            status_class = "status-cross"
                                        tracker_form_data += f"""
                                        <tr>
                                            <td class="center-align">AD{idx:03d}</td>
                                            <td class="left-align">{doc_name}</td>
                                            <td class="center-align"><i class="fas fa-{status_icon} status-icon {status_class}"></i></td>
                                        </tr>
                                        """
                                elif app_type == "Revalidation":
                                    reval_doc_names = [
                                        doc_name for doc_name in reval_docs.values()
                                    ]
                                    for idx, doc_name in enumerate(
                                        reval_doc_names, start=1
                                    ):
                                        if data[f"REQ{idx:03d}"]["approved"] == "1":
                                            status_icon = "check"
                                            status_class = "status-check"
                                        else:
                                            status_icon = "times"
                                            status_class = "status-cross"
                                        tracker_form_data += f"""
                                        <tr>
                                            <td class="center-align">RD{idx:03d}</td>
                                            <td class="left-align">{doc_name}</td>
                                            <td class="center-align"><i class="fas fa-{status_icon} status-icon {status_class}"></i></td>
                                        </tr>
                                        """
                            with tracker_form.container():
                                st.subheader("📝 Evaluation Tracker")
                                st.markdown(
                                    f"""
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
                                                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
                                                    <th colspan="3" class="center-align">{filename}</th>
                                                </tr>
                                                <tr>
                                                    <th class="center-align">Code</th>
                                                    <th class="left-align">Form Name</th>
                                                    <th class="center-align">Status</th>
                                                </tr>
                                                
                                                {tracker_form_data}
                                            """,
                                    unsafe_allow_html=True,
                                )

                    if save_btn:
                        if any(
                            not doc_data["remark"] for doc_data in eval_data.values()
                        ):
                            sac.alert(
                                label="Please provide remarks for all documents.",
                                size="sm",
                                variant="quote-light",
                                color="info",
                                icon=True,
                            )
                        else:
                            tracker_form.empty()
                            st.session_state["show_eval_summary"] = True

                    if st.session_state["show_eval_summary"]:
                        with cols[1]:
                            st.subheader("⭐ Evaluation Summary")
                            eval_summary = pd.DataFrame(eval_data).T
                            # Rename the columns
                            eval_summary.rename(
                                columns={"approved": "Approved", "remark": "Remarks"},
                                inplace=True,
                            )

                            # Replace True/False in the 'Approved' column with '✅' and '❌'
                            eval_summary["Approved"] = eval_summary["Approved"].replace(
                                {True: "✅", False: "❌"}
                            )
                            st.table(eval_summary)

                            if eval_phase == "IE":
                                sac.alert(
                                    label="Once you click on confirm, your evaluation will be submitted and transferred to your final evaluator.",
                                    size="sm",
                                    variant="quote-light",
                                    color="info",
                                    icon=True,
                                )
                                new_status = "Final Evaluation"
                            elif eval_phase == "FE":
                                new_status = sac.chip(
                                    items=[
                                        sac.ChipItem(
                                            label="Returned for Revisions",
                                            icon="bi bi-arrow-counterclockwise",
                                        ),
                                        sac.ChipItem(
                                            label="Chairperson's Approval",
                                            icon="bi bi-check-circle",
                                        ),
                                    ],
                                    label="Status",
                                    description="Once you click on confirm, your evaluation will be submitted and transferred to the next phase.",
                                    index=2,
                                    align="start",
                                    radius="md",
                                    variant="light",
                                )
                            elif eval_phase == "CA":
                                new_status = sac.chip(
                                    items=[
                                        sac.ChipItem(
                                            label="Returned for Revisions",
                                            icon="bi bi-arrow-counterclockwise",
                                        ),
                                        sac.ChipItem(
                                            label="Approved", icon="bi bi-check-circle"
                                        ),
                                        sac.ChipItem(
                                            label="Rejected", icon="bi bi-x-circle"
                                        ),
                                    ],
                                    label="Status",
                                    description="Once you click on confirm, your evaluation and remarks will be returned to the organization.",
                                    index=3,
                                    align="start",
                                    radius="md",
                                    variant="light",
                                )
                                chair_remarks = st.text_area('**Chairperson\'s Remarks**', placeholder='Input remarks here...', height=100)

                            if new_status == "Final Evaluation":
                                next_eval_phase = "FE"
                            elif new_status == "Chairperson's Approval":
                                next_eval_phase = "CA"
                            elif new_status == "Returned for Revisions":
                                next_eval_phase = "Returned"
                            elif new_status == "Approved":
                                next_eval_phase = "Approved"
                            elif new_status == "Rejected":
                                next_eval_phase = "Rejected"

                            
                            if eval_phase == "CA":
                                confirm_btn = st.button(
                                    "Confirm Evaluation", disabled=not new_status and not chair_remarks
                                )
                            else:
                                confirm_btn = st.button(
                                    "Confirm Evaluation", disabled=not new_status
                                )
                            if confirm_btn:
                                msg = st.toast("Submitting Evaluation...", icon="🔃")

                                # Save evaluation data to database
                                with st.spinner(
                                    "Submitting Organization Evaluation..."
                                ):
                                    if str(app_type) == "Accreditation":
                                        response_code = submit_evaluation_accre(
                                            sub_to_eval, eval_data
                                        )
                                    elif str(app_type) == "Revalidation":
                                        response_code = submit_evaluation_reval(
                                            sub_to_eval, eval_data
                                        )
                                    if response_code:
                                        modify_eval_phase(sub_to_eval, next_eval_phase)
                                        update_last_updated(sub_to_eval)

                                        # If submission is returned, approved, or rejected, send notification email
                                        if next_eval_phase in [
                                            "Returned",
                                            "Approved",
                                            "Rejected",
                                        ]:
                                            email = get_email(username)
                                            abbreviation = get_abbreviation(username)
                                            send_notif_email(
                                                email, abbreviation, app_type, app_order
                                            )

                                        time.sleep(2)
                                        msg.toast(
                                            "Evaluation submitted successfully.",
                                            icon="✅",
                                        )
                                        st.session_state["show_eval_summary"] = False
                                        sac.alert(
                                            label="Evaluation submitted successfully.",
                                            size="sm",
                                            variant="quote-light",
                                            color="success",
                                            icon=True,
                                        )
                                        st.button("Evaluate Another Organization", on_click=evaluate_another_org)
                                            

        else:
            sac.result(
                label="No Results Found",
                description="We couldn't locate any matching submissions.",
                status="empty",
            )

if __name__ == "__main__":
    view_submissions()