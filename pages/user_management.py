import streamlit as st
import streamlit_antd_components as sac
from helpers import fetch_data, modify_user_data, assign_roles
import pandas as pd

def user_management():
    st.header("👤 User Management")
    users = fetch_data('https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_user_data')

    user_data_columns = [col['col'] for col in users['data']['columns']]

    columns_to_show = sac.checkbox(
        items=user_data_columns,
        label='**User Data Columns**', description='Click on the checkbox to toggle which columns to show', index=[1,2,3,4], align='start', size='sm', check_all='Select all', 
    )

    if columns_to_show:
        user_data = pd.DataFrame(users['data']['rows'], columns=columns_to_show)
        st.dataframe(user_data, hide_index=True)

    tab = sac.tabs([
        sac.TabsItem(label='Modify User Data'),
        sac.TabsItem(label='Assign Roles'),
    ], align='start', variant='outline', size='sm')

    if columns_to_show == []:
        sac.result(label='No columns selected.', description='Please select a column to see your data.', status='empty')
    else:
        col1, col2 = st.columns([0.2, 0.8], vertical_alignment='center')
        if tab == 'Modify User Data':
            with col1:
                identifier = st.radio('**Select by:**', [col for col in columns_to_show if col not in ['role', 'last_login', 'created_at']])
                to_modify = st.radio('**Modify:**', [col for col in columns_to_show if col not in ['username', 'role', 'last_login', 'created_at']])
            with col2:
                identifier_value = st.selectbox(f'**Select {identifier}**', user_data[identifier].unique())
                if to_modify == None:
                    st.info("Please select a column to modify.")
                else:
                    new_value = st.text_input(f'**New {to_modify}**')
                    modify_data = st.button("Modify Data")
                    if modify_data:
                        affected_rows = modify_user_data(identifier, to_modify, identifier_value, new_value)
                        st.toast(f"Successfully modified {affected_rows} row(s).", icon="✅")

        if tab == 'Assign Roles':
            with st.container(border=True):
                with col1:
                    identifier = st.radio('**Select by:**', [col for col in columns_to_show if col not in ['role', 'last_login', 'created_at']])
                with col2:
                    if 'role' not in columns_to_show:
                        identifier_value = st.multiselect(f'**Select {identifier}**', user_data[identifier].unique(), disabled=True)
                        assigned_role = st.selectbox('**Assign Role:**', ['user', 'cosoa', 'execcomm', 'chair'], disabled=True)
                        assign_role = st.button("Assign Role", disabled=True)
                        st.warning("Please select the 'role' column to assign roles.")
                    else:
                        identifier_value = st.multiselect(f'**Select {identifier}**', user_data[identifier].unique())
                        assigned_role = st.selectbox('**Assign Role:**', ['user', 'cosoa', 'execcomm', 'chair'])
                        assign_role = st.button("Assign Role")
                        if assign_role:
                            affected_rows = assign_roles(identifier, identifier_value, assigned_role)
                            st.toast(f"Successfully assigned {affected_rows} row(s) to {assigned_role}.", icon="✅")
        with col1:
            st.button("Refresh Data", help="Refresh the data to see the changes made.")