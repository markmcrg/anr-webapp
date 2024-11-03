import streamlit as st
import streamlit_antd_components as sac
from helpers import fetch_data, modify_user_data, assign_roles, update_settings
import pandas as pd

def user_management():
    with st.container(border=True):
        st.header("👤 User Management")
        users = fetch_data('https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_user_data')

        user_data_columns = [col['col'] for col in users['data']['columns']]
        col1, col2 = st.columns([7, 3], vertical_alignment='center')
        with col1:
            columns_to_show = sac.checkbox(
                items=user_data_columns,
                label='**User Data Columns**', description='Click on the checkbox to toggle which columns to show', index=[1,2,3,4], align='start', size='sm', 
            )
        if 'role' in columns_to_show:
            with col2:
                role_filter = sac.checkbox(
                    items=['enbanc', 'cosoa', 'user'],
                    label='**Role Columns**', description='Click on the checkbox to toggle which roles to show', index=[0,1,2], align='start', size='sm', 
                )
        
        
        if columns_to_show and role_filter:
            user_data = pd.DataFrame(users['data']['rows'], columns=columns_to_show)
            user_data = user_data[user_data['role'].isin(role_filter)]
            st.dataframe(user_data, hide_index=True)
        elif columns_to_show:
            user_data = pd.DataFrame(users['data']['rows'], columns=columns_to_show)
            st.dataframe(user_data, hide_index=True)

        tab = sac.tabs([
            sac.TabsItem(label='Modify User Data'),
            sac.TabsItem(label='Assign Roles'),
            sac.TabsItem(label='Toggle Settings'),
        ], align='start', variant='outline', size='sm')

        if columns_to_show == []:
            sac.result(label='No columns selected.', description='Please select a column to see your data.', status='empty')
        else:
            col1, col2 = st.columns([0.2, 0.8], vertical_alignment='center')
            if tab == 'Modify User Data':
                if set(columns_to_show).issubset({'role', 'last_login', 'created_at'}):
                        st.info("Please select an identifier column to modify the data.")
                else:
                    with col1:
                            identifier = st.radio('**Select by:**', [col for col in columns_to_show if col not in ['role', 'last_login', 'created_at']])
                            to_modify = st.radio('**Modify:**', [col for col in columns_to_show if col not in ['username', 'role', 'last_login', 'created_at']])
                            st.button("Refresh Data", help="Refresh the data to see the changes made.")
                    with col2:
                        identifier_value = st.selectbox(f'**Select {identifier}**', user_data[identifier].unique())
                        if to_modify is None:
                            st.info("Please select a column to modify.")
                        else:
                            new_value = st.text_input(f'**New {to_modify}**')
                            modify_data = st.button("Modify Data")
                            if modify_data:
                                affected_rows = modify_user_data(identifier, to_modify, identifier_value, new_value)
                                st.toast(f"Successfully modified {affected_rows} row(s).", icon="✅")

            if tab == 'Assign Roles':
                if set(columns_to_show).issubset({'role', 'last_login', 'created_at'}):
                    st.info("Please select an identifier column to assign roles.")
                else:
                    with col1:
                        identifier = st.radio('**Select by:**', [col for col in columns_to_show if col not in ['role', 'last_login', 'created_at']])
                        st.button("Refresh Data", help="Refresh the data to see the changes made.")
                    with col2:
                        if 'role' not in columns_to_show:
                            identifier_value = st.multiselect(f'**Select {identifier}**', user_data[identifier].unique(), disabled=True)
                            assigned_role = st.selectbox('**Assign Role:**', ['user', 'cosoa', 'enbanc', 'chair'], disabled=True)
                            assign_role = st.button("Assign Role", disabled=True)
                            st.warning("Please select the 'role' column to assign roles.")
                        else:
                            identifier_value = st.multiselect(f'**Select {identifier}**', user_data[identifier].unique())
                            assigned_role = st.selectbox('**Assign Role:**', ['user', 'cosoa', 'enbanc', 'chair'])
                            assign_role = st.button("Assign Role")
                            if assign_role:
                                affected_rows = assign_roles(identifier, identifier_value, assigned_role)
                                st.toast(f"Successfully assigned {affected_rows} row(s) to {assigned_role}.", icon="✅")
            if tab == "Toggle Settings":
                settings = fetch_data('https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_settings')['data']['rows']
                if settings:
                    toggle_submissions = st.toggle("Toggle Submissions", value= True if settings[1]['status'] == "TRUE" else False)
                    toggle_resubmissions = st.toggle("Toggle Resubmissions", value= True if settings[0]['status'] == "TRUE" else False)
                    
                    # Show update button if changes have been made
                    update_settings_btn = st.button("Update Settings")
                    if update_settings_btn:
                        if toggle_submissions:
                            update_settings('accepting_submissions', "TRUE")
                        else:
                            update_settings('accepting_submissions', "FALSE")
                        if toggle_resubmissions:
                            update_settings('accepting_resubmissions', "TRUE")
                        else:
                            update_settings('accepting_resubmissions', "FALSE")
                            
                        sac.alert(label='Settings updated successfully.', size='sm', variant='quote-light', color='success', icon=True)
                else:
                    st.warning("No settings found.")

        