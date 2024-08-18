import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import streamlit_antd_components as sac
import mailtrap as mt
import json
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timezone, timedelta
from b2sdk.v2 import InMemoryAccountInfo, B2Api, UploadSourceBytes

# Function to fetch data from the TiDB Cloud API
@st.cache_data(show_spinner=False)
def fetch_data(url: str) -> dict:
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))
    return response.json()

def unpack_credentials(user_data: dict) -> dict:
    user_data_df = pd.DataFrame(user_data['rows'], columns=[col['col'] for col in user_data['columns']])
    emails = user_data_df['email'].tolist()
    passwords = user_data_df['password'].tolist()
    org_names = user_data_df['org_name'].tolist()
    created_at = user_data_df['created_at'].tolist()
    last_login = user_data_df['last_login'].tolist()
    usernames = user_data_df['username'].tolist()
    roles = user_data_df['role'].tolist()
    
    credentials = {
        'usernames': {}
    }
    for username, email, password, org_name in zip(usernames, emails, passwords, org_names):
        credentials['usernames'][username] = {
            'email': email,
            'failed_login_attempts': 0,
            'logged_in': False,
            'name': org_name,
            'password': password
        }

    return credentials


# I can make a render menu helper function to render the menu for each page along with conditions on what to show depending on the user's role and login status
def render_menu(active_index, role, login_status):
    with st.sidebar:
        menu_item = sac.menu([
            sac.MenuItem('Home', icon='house-fill', ),
            sac.MenuItem('Accredited Organizations', icon='card-list'),
            sac.MenuItem('Application Requirements', icon='file-earmark-text-fill'),
            sac.MenuItem('Frequently Asked Questions', icon='question-circle-fill'),
            sac.MenuItem('Sign Up', icon='door-open-fill'),
            sac.MenuItem('Login', icon='door-closed-fill'),

        ], open_all=False, index=active_index, return_index=True)
        return menu_item
    
def page_router(active_index, current_index):
    if active_index != current_index:
        if active_index == 1:
            st.switch_page('pages/accredited_orgs.py')
        elif active_index == 0:
            st.switch_page('main.py')

def register_user(email, password, org_name, username, abbreviation):
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key

    url = 'https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/users'

    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        "abbreviation": abbreviation,
        "email": email,
        "entered_pass": password,
        "org_name": org_name,
        "username": username
    }

    response = requests.post(url, headers=headers, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY), data=json.dumps(data))

    if response.status_code == 200:
        return True
    else:
        return False

def check_username(username):
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key
    
    url = f'https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/check_username?username={username}'
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    response_dict['data']['rows']

    if response_dict['data']['rows']:
        return True
    else:
        return False
    
def check_email(email):
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key
    
    url = f'https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/check_email?email={email}'
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    response_dict['data']['rows']

    if response_dict['data']['rows']:
        return True
    else:
        return False
    
def send_otp_email(email, otp, name):
    mail = mt.MailFromTemplate(
        sender=mt.Address(email='no-reply@sccosoa.com', name='PUP SC COSOA'),
        to=[mt.Address(email=email)],
        template_uuid=st.secrets.mailtrap_creds.template_uuid,
        template_variables={
        'name': name,
        'otp': otp
        }
    )
    # create client and send
    try:
        client = mt.MailtrapClient(token=st.secrets.mailtrap_creds.token)
        client.send(mail)
        return True
    except:
        return False
    
def get_role(username):
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key
    
    url = f'https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_role?username={username}'
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    response_dict['data']['rows']
    
    # Return the role of the user
    try:
        return response_dict['data']['rows'][0]['role']
    except:
        return None

@st.cache_data(show_spinner=False)
def get_abbreviation(username):
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key
    
    url = f'https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_abbreviation?username={username}'
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    response_dict['data']['rows']
    
    # Return the abbreviation of the user
    try:
        return response_dict['data']['rows'][0]['abbreviation']
    except:
        return None
    
def get_email(username):
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key
    
    url = f'https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_email?username={username}'
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    response_dict['data']['rows']
    
    # Return the email of the user
    try:
        return response_dict['data']['rows'][0]['email']
    except:
        return None
    
def get_name(username):
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key
    
    url = f'https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_org_name?username={username}'
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    response_dict['data']['rows']
    
    # Return the org_name of the user
    try:
        return response_dict['data']['rows'][0]['org_name']
    except:
        return None
def get_password(username):
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key
    
    url = f'https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_pw?username={username}'
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    response_dict['data']['rows']
    
    # Return the password of the user
    try:
        return response_dict['data']['rows'][0]['password']
    except:
        return None
    
def update_last_login(username):
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key
    
    url = 'https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/update_last_login'
    headers = {
    'content-type': 'application/json',
    }

    data = {
        "username": username
    }
    response = requests.put(url, headers=headers, json=data, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    if response.status_code == 200:
        return True
    else:
        return False

def modify_user_data(identifier, to_modify, identifier_value, new_value):
    try:
        connection = mysql.connector.connect(
            host=st.secrets['anr_webapp_db']['host'],
            user=st.secrets['anr_webapp_db']['user'],
            port=st.secrets['anr_webapp_db']['port'],
            password=st.secrets['anr_webapp_db']['password'],
            database=st.secrets["anr_webapp_db"]["database"],
        )
    except Error as e:
        st.error(f"The error '{e}' occurred")
    cursor = connection.cursor()
    cursor.execute(f"UPDATE users SET {to_modify} = '{new_value}' WHERE {identifier} = '{identifier_value}'")
    affected_rows = cursor.rowcount
    connection.commit()
    cursor.close()
    connection.close()
    return affected_rows

def assign_roles(identifier, identifier_values, role):
    try:
        connection = mysql.connector.connect(
            host=st.secrets['anr_webapp_db']['host'],
            user=st.secrets['anr_webapp_db']['user'],
            port=st.secrets['anr_webapp_db']['port'],
            password=st.secrets['anr_webapp_db']['password'],
            database=st.secrets["anr_webapp_db"]["database"],
        )
    except Error as e:
        st.error(f"The error '{e}' occurred")
    cursor = connection.cursor()
    query = f"UPDATE users SET role = '{role}' WHERE {identifier} IN (%s)" % ','.join(['%s'] * len(identifier_values))

    # Execute the query with the email list
    cursor.execute(query, tuple(identifier_values))
    affected_rows = cursor.rowcount
    connection.commit()
    cursor.close()
    connection.close()
    return affected_rows
# @st.cache_data(show_spinner=False)
def get_app_orders(username):
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key
    
    url = f'https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_app_orders?username={username}'
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    app_orders = response_dict['data']['rows'][0]
    
    return app_orders

# @st.cache_data(show_spinner=False)
def get_app_type(username):
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key
    
    url = f'https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_app_type?username={username}'
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    app_type = response_dict['data']['rows'][0]['app_type']
    
    return app_type


def authenticate_b2(bucket_name):
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    application_key_id = st.secrets['b2_user_app_key']['keyID']
    application_key = st.secrets['b2_user_app_key']['applicationKey']
    b2_api.authorize_account("production", application_key_id, application_key)
    bucket = b2_api.get_bucket_by_name(bucket_name)
    return bucket

def upload_document(bucket, uploaded_file, file_name):
    if not file_name.lower().endswith('.pdf'):
        file_name += '.pdf'
        
    file_bytes = uploaded_file.read()
    upload_source = UploadSourceBytes(file_bytes)
    file_ver = bucket.upload(upload_source, file_name, content_type='application/pdf')
    
    return file_ver

def list_files(bucket):
    # List all files in the bucket
    for file_version, folder_name in bucket.ls(latest_only=False, recursive=True):
        # Convert upload timestamp epoch to human-readable format
        epoch_timestamp = file_version.upload_timestamp / 1000
        upload_timestamp = datetime.fromtimestamp(epoch_timestamp, timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
        st.write(f'**{file_version.file_name}** | {upload_timestamp}')

def get_download_url(bucket, filename, auth=True):
    download_auth_token = bucket.get_download_authorization(filename, 3600) # Modfiy this to change depending on filename and access
    download_url = bucket.get_download_url(filename)
    if auth:
        auth_download_url = str(f"{download_url}?Authorization={download_auth_token}")
        return auth_download_url
    else:
        return download_url

def record_submission(filename, org_name, app_type, app_order, jurisdiction, b2_file_url):
    PUBLIC_KEY = st.secrets.tidb_keys.public_key
    PRIVATE_KEY = st.secrets.tidb_keys.private_key

    url = 'https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/record_submission'

    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        "app_order": app_order,
        "app_type": app_type,
        "b2_file_url": b2_file_url,
        "filename": filename,
        "jurisdiction": jurisdiction,
        "org_name": org_name
    }

    response = requests.post(url, headers=headers, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY), data=json.dumps(data))

    if response.status_code == 200:
        return True
    else:
        return False