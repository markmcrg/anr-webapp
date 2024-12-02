import streamlit as st
import pandas as pd
import time
import re

# # # Add the main directory to the system path if necessary
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helpers import fetch_data, edit_chair_remarks, publish_org


def get_abbreviation(text):
    match = re.search(r"\(([^)]+)\)", text)
    return match.group(1) if match else None


def get_org_details(org_name, approved_sub_df):
    org_data = approved_sub_df[approved_sub_df["org_name"] == org_name].iloc[0]
    return org_data["jurisdiction"], org_data["app_type"]


def approved_orgs():
    with st.container(border=True):
        submission_data = fetch_data(
            "https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_all_submissions_with_chair_remarks"
        )["data"]["rows"]

        sub_df = pd.DataFrame(submission_data)
        approved_sub_df = sub_df[sub_df["eval_phase"] == "Approved"]

        approved_sub_df["date_submitted"] = pd.to_datetime(
            approved_sub_df["date_submitted"]
        )
        approved_sub_df = approved_sub_df.sort_values(
            by="date_submitted", ascending=True
        )

        st.subheader("🏆 Approved Organizations")
        approved_sub_df = approved_sub_df[
            [
                "filename",
                "org_name",
                "jurisdiction",
                "app_type",
                "chair_remarks",
                "date_submitted",
            ]
        ]

        display_df = approved_sub_df[
            [
                "date_submitted",
                "filename",
                "org_name",
                "jurisdiction",
                "app_type",
                "chair_remarks",
            ]
        ].rename(
            columns={
                "date_submitted": "Date Submitted",
                "filename": "File Name",
                "org_name": "Organization Name",
                "jurisdiction": "Jurisdiction",
                "app_type": "Application Type",
                "chair_remarks": "Chair's Remarks",
            }
        )

        st.dataframe(
            display_df,
            hide_index=True,
            column_config={
                "Date Submitted": st.column_config.DatetimeColumn(
                    format="D MMM YYYY, h:mm a", timezone="Asia/Manila"
                )
            },
        )

        st.write("---")

        cols = st.columns([1, 1], gap="medium")
        with cols[0]:
            st.write("#### ➕ Publish New Organization")
            published_orgs = fetch_data(
                "https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/accredited_orgs_2425"
            )["data"]

            filtered_approved_sub_df = approved_sub_df[
                ~approved_sub_df["org_name"].isin(
                    [org["org_name"] for org in published_orgs["rows"]]
                )
            ]
            selected_orgs = st.multiselect(
                "**Select an organization**",
                filtered_approved_sub_df["org_name"],
                placeholder="Select organizations...",
            )
            if st.checkbox("View published organizations", key="view_published"):
                display_published_df = pd.DataFrame(published_orgs["rows"])

                display_published_df = display_published_df.rename(
                    columns={
                        "socn": "SOCN",
                        "org_name": "Organization Name",
                        "jurisdiction": "Jurisdiction",
                        "status": "Type",
                    }
                )
                st.dataframe(
                    display_published_df,
                    hide_index=True,
                    column_order=["SOCN", "Organization Name", "Jurisdiction", "Type"],
                )
            cols2 = st.columns([1, 1, 1])
            for org in selected_orgs:
                with cols2[0]:
                    abbreviation = get_abbreviation(org)
                    st.text_input(
                        "**Abbreviation**",
                        value=abbreviation,
                        disabled=True,
                        key=f"{org}_abbreviation",
                    )
                with cols2[1]:
                    jurisdiction, app_type = get_org_details(org, approved_sub_df)
                    st.text_input(
                        "**Jurisdiction**",
                        value=jurisdiction,
                        disabled=True,
                        key=f"{org}_jurisdiction",
                    )
                with cols2[2]:
                    st.text_input(
                        "**Application Type**",
                        value=app_type,
                        disabled=True,
                        key=f"{org}_app_type",
                    )

            org_count = len(published_orgs["rows"])

            def format_socn(org, count):
                jurisdiction, app_type = get_org_details(org, approved_sub_df)
                socn_app_type = "A" if app_type == "Accreditation" else "R"
                socn_jurisdiction = (
                    "UWIDE" if jurisdiction == "U-WIDE" else jurisdiction
                )
                return {
                    "SOCN": f"2425-{str(count).zfill(3)}-{socn_app_type}-{socn_jurisdiction}",
                    "Organization Name": org,
                    "Jurisdiction": jurisdiction,
                    "Type": app_type,
                }

            generated_orgs = [
                format_socn(org, org_count + i + 1)
                for i, org in enumerate(selected_orgs)
            ]

            if generated_orgs:
                st.dataframe(
                    pd.DataFrame(generated_orgs),
                    hide_index=True,
                    use_container_width=True,
                )

            publish_btn = st.button("Publish Organization", disabled=not generated_orgs)
            if publish_btn:
                progress_text = "Publishing organizations..."
                my_bar = st.progress(0, text=progress_text)

                total_items = len(generated_orgs)
                for idx, item in enumerate(generated_orgs):
                    if item["Type"] == "Accreditation":
                        status = "Accredited"
                    else:
                        status = "Revalidated"
                    publish_org(
                        item["SOCN"],
                        item["Organization Name"],
                        item["Jurisdiction"],
                        status,
                    )
                    # Update progress bar
                    my_bar.progress((idx + 1) / total_items, text=progress_text)

                st.toast("Organization successfully published!", icon="✅")
                st.success("All organizations have been successfully published.")

                if st.button("Reload"):
                    st.rerun()

        with cols[1]:
            st.write("#### 📝 Edit Remarks")

            selected_sub = st.selectbox(
                "**Select a submission**", approved_sub_df["filename"]
            )
            selected_data = approved_sub_df[approved_sub_df["filename"] == selected_sub]

            st.text_area(
                "**Remarks**",
                value=selected_data["chair_remarks"].values[0],
                disabled=True,
                height=75,
            )
            new_remarks = st.text_area(
                "**Edit Remarks**", placeholder="Input new remarks here...", height=75
            )

            edit_btn = st.button("Edit Remarks", disabled=not new_remarks)
            if edit_btn:
                if edit_chair_remarks(selected_data["filename"].values[0], new_remarks):
                    st.toast("Remarks successfully edited! Reloading...", icon="✅")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("An error occurred while editing the remarks.")


if __name__ == "__main__":
    approved_orgs()
