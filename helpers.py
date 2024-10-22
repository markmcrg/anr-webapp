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
import streamlit_antd_components as sac
import os

# Function to fetch data from the TiDB Cloud API
def fetch_data(url: str) -> dict:
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))
    return response.json()

def page_router(active_index, current_index):
    if active_index != current_index:
        if active_index == 1:
            st.switch_page("pages/accredited_orgs.py")
        elif active_index == 0:
            st.switch_page("main.py")


def register_user(email, password, org_name, username, abbreviation):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = "https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/users"

    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "abbreviation": abbreviation,
        "email": email,
        "entered_pass": password,
        "org_name": org_name,
        "username": username,
    }

    response = requests.post(
        url,
        headers=headers,
        auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY),
        data=json.dumps(data),
    )

    if response.status_code == 200:
        return True
    else:
        return False


def check_username(username):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = f"https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/check_username?username={username}"
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    response_dict["data"]["rows"]

    if response_dict["data"]["rows"]:
        return True
    else:
        return False


def check_email(email):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = f"https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/check_email?email={email}"
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    response_dict["data"]["rows"]

    if response_dict["data"]["rows"]:
        return True
    else:
        return False


def send_otp_email(email, otp, name):
    mail = mt.MailFromTemplate(
        sender=mt.Address(email="no-reply@sccosoa.com", name="PUP SC COSOA"),
        to=[mt.Address(email=email)],
        template_uuid=os.environ['mt_otp_template_uuid'],
        template_variables={"name": name, "otp": otp},
    )
    # create client and send
    try:
        client = mt.MailtrapClient(token=os.environ['mt_token'])
        client.send(mail)
        return True
    except:
        return False


def send_notif_email(email, name, app_type, app_order):
    mail = mt.MailFromTemplate(
        sender=mt.Address(email="no-reply@sccosoa.com", name="PUP SC COSOA"),
        to=[mt.Address(email=email)],
        template_uuid=os.environ['mt_notif_template_uuid'],
        template_variables={
            "name": name,
            "app_type": app_type,
            "app_order": app_order,
        },
    )
    # create client and send
    try:
        client = mt.MailtrapClient(token=os.environ['mt_token'])
        client.send(mail)
        return True
    except:
        return False


def get_role(username):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = f"https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_role?username={username}"
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    response_dict["data"]["rows"]

    # Return the role of the user
    try:
        return response_dict["data"]["rows"][0]["role"]
    except:
        return None


@st.cache_data(show_spinner=False)
def get_abbreviation(username):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = f"https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_abbreviation?username={username}"
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    response_dict["data"]["rows"]

    # Return the abbreviation of the user
    try:
        return response_dict["data"]["rows"][0]["abbreviation"]
    except:
        return None


def get_email(username):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = f"https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_email?username={username}"
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    response_dict["data"]["rows"]

    # Return the email of the user
    try:
        return response_dict["data"]["rows"][0]["email"]
    except:
        return None


def get_name(username):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = f"https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_org_name?username={username}"
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    response_dict["data"]["rows"]

    # Return the org_name of the user
    try:
        return response_dict["data"]["rows"][0]["org_name"]
    except:
        return None


def get_password(username):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = f"https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_pw?username={username}"
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    response_dict["data"]["rows"]

    # Return the password of the user
    try:
        return response_dict["data"]["rows"][0]["password"]
    except:
        return None


def update_last_login(username):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = "https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/update_last_login"
    headers = {
        "content-type": "application/json",
    }

    data = {"username": username}
    response = requests.put(
        url, headers=headers, json=data, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY)
    )

    if response.status_code == 200:
        return True
    else:
        return False
    
def update_last_updated(filename):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = "https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/update_last_updated"
    headers = {
        "content-type": "application/json",
    }

    data = {"filename": filename}
    response = requests.put(
        url, headers=headers, json=data, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY)
    )

    if response.status_code == 200:
        return True
    else:
        return False


def modify_user_data(identifier, to_modify, identifier_value, new_value):
    try:
        connection = mysql.connector.connect(
            host=os.environ['db1_host'],
            user=os.environ['db1_user'],
            port=os.environ['db1_port'],
            password=os.environ['db1_password'],
            database=os.environ['db1_database'],
        )
    except Error as e:
        st.error(f"The error '{e}' occurred")
    cursor = connection.cursor()
    cursor.execute(
        f"UPDATE users SET {to_modify} = '{new_value}' WHERE {identifier} = '{identifier_value}'"
    )
    affected_rows = cursor.rowcount
    connection.commit()
    cursor.close()
    connection.close()
    return affected_rows


def assign_roles(identifier, identifier_values, role):
    try:
        connection = mysql.connector.connect(
            host=os.environ['db1_host'],
            user=os.environ['db1_user'],
            port=os.environ['db1_port'],
            password=os.environ['db1_password'],
            database=os.environ['db1_database'],
        )
    except Error as e:
        st.error(f"The error '{e}' occurred")
    cursor = connection.cursor()
    query = f"UPDATE users SET role = '{role}' WHERE {identifier} IN (%s)" % ",".join(
        ["%s"] * len(identifier_values)
    )

    # Execute the query with the email list
    cursor.execute(query, tuple(identifier_values))
    affected_rows = cursor.rowcount
    connection.commit()
    cursor.close()
    connection.close()
    return affected_rows

def get_app_orders(username):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = f"https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_app_orders?username={username}"
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    app_orders = response_dict["data"]["rows"][0]

    return app_orders

def get_app_type(username):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = f"https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_app_type?username={username}"
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    app_type = response_dict["data"]["rows"][0]["app_type"]

    return app_type

def authenticate_b2(bucket_name):
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    application_key_id = os.environ['b2_keyID']
    application_key = os.environ['b2_applicationKey']
    b2_api.authorize_account("production", application_key_id, application_key)
    bucket = b2_api.get_bucket_by_name(bucket_name)
    return bucket


def upload_document(bucket, uploaded_file, file_name):
    if not file_name.lower().endswith(".pdf"):
        file_name += ".pdf"

    file_bytes = uploaded_file.read()
    upload_source = UploadSourceBytes(file_bytes)
    file_ver = bucket.upload(upload_source, file_name, content_type="application/pdf")

    return file_ver


def list_files(bucket):
    # List all files in the bucket
    for file_version, folder_name in bucket.ls(latest_only=False, recursive=True):
        # Convert upload timestamp epoch to human-readable format
        epoch_timestamp = file_version.upload_timestamp / 1000
        upload_timestamp = datetime.fromtimestamp(
            epoch_timestamp, timezone(timedelta(hours=8))
        ).strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"**{file_version.file_name}** | {upload_timestamp}")

def get_download_url(_bucket, filename, auth=True):
    download_auth_token = _bucket.get_download_authorization(
        filename, 86400
    )  # Modfiy this to change depending on filename and access
    download_url = _bucket.get_download_url(filename)
    if auth:
        auth_download_url = str(f"{download_url}?Authorization={download_auth_token}")
        return auth_download_url
    else:
        return download_url

def record_submission(
    filename, org_name, app_type, app_order, jurisdiction, b2_file_url, username
):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = "https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/record_submission"

    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "app_order": app_order,
        "app_type": app_type,
        "b2_file_url": b2_file_url,
        "filename": filename,
        "jurisdiction": jurisdiction,
        "org_name": org_name,
        "username": username,
    }

    response = requests.post(
        url,
        headers=headers,
        auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY),
        data=json.dumps(data),
    )

    if response.status_code == 200:
        return True
    else:
        return False


def get_submissions(username):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = f"https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_submissions?username={username}"
    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()
    submissions = response_dict["data"]["rows"]

    return submissions


def get_abbreviation_from_webmail(webmail):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = f"https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/get_abbreviation_from_webmail?email={webmail}"

    response = requests.get(url, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY))

    # Turn the response into a dictionary
    response_dict = response.json()

    try:
        return response_dict["data"]["rows"][0]["abbreviation"]
    except:
        return None


def update_settings(setting, status):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = "https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/change_settings"
    headers = {
        "content-type": "application/json",
    }

    data = {"setting": setting, "status": status}

    response = requests.put(
        url, headers=headers, json=data, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY)
    )

    if response.status_code == 200:
        return True
    else:
        return False


def submit_evaluation_accre(filename, eval_data):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = "https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/evaluate_org_accre"

    headers = {
        "content-type": "application/json",
    }

    # Convert the 'approved' values from boolean to integer
    for key in eval_data:
        eval_data[key]["approved"] = int(eval_data[key]["approved"])

    data = {
        "req001_approved": eval_data["AD001"]["approved"],
        "req001_remarks": eval_data["AD001"]["remark"],
        "req002_approved": eval_data["AD002"]["approved"],
        "req002_remarks": eval_data["AD002"]["remark"],
        "req003_approved": eval_data["AD003"]["approved"],
        "req003_remarks": eval_data["AD003"]["remark"],
        "req004_approved": eval_data["AD004"]["approved"],
        "req004_remarks": eval_data["AD004"]["remark"],
        "req005_approved": eval_data["AD005"]["approved"],
        "req005_remarks": eval_data["AD005"]["remark"],
        "filename": filename,
    }
    response = requests.put(
        url, headers=headers, json=data, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY)
    )

    return response.json()


def submit_evaluation_reval(filename, eval_data):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = "https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/evaluate_org_reval"

    headers = {
        "content-type": "application/json",
    }

    # Convert the 'approved' values from boolean to integer
    for key in eval_data:
        eval_data[key]["approved"] = int(eval_data[key]["approved"])

    data = {
        "req001_approved": eval_data["RD001"]["approved"],
        "req001_remarks": eval_data["RD001"]["remark"],
        "req002_approved": eval_data["RD002"]["approved"],
        "req002_remarks": eval_data["RD002"]["remark"],
        "req003_approved": eval_data["RD003"]["approved"],
        "req003_remarks": eval_data["RD003"]["remark"],
        "req004_approved": eval_data["RD004"]["approved"],
        "req004_remarks": eval_data["RD004"]["remark"],
        "req005_approved": eval_data["RD005"]["approved"],
        "req005_remarks": eval_data["RD005"]["remark"],
        "req006_approved": eval_data["RD006"]["approved"],
        "req006_remarks": eval_data["RD006"]["remark"],
        "req007_approved": eval_data["RD007"]["approved"],
        "req007_remarks": eval_data["RD007"]["remark"],
        "req008_approved": eval_data["RD008"]["approved"],
        "req008_remarks": eval_data["RD008"]["remark"],
        "filename": filename,
    }

    response = requests.put(
        url, headers=headers, json=data, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY)
    )

    if response.status_code == 200:
        return True
    else:
        return False


def modify_eval_phase(filename, eval_phase="FE"):
    PUBLIC_KEY = os.environ['tidb_public_key']
    PRIVATE_KEY = os.environ['tidb_private_key']

    url = "https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/dataapp-SxHAXFax/endpoint/modify_eval_phase"

    headers = {
        "content-type": "application/json",
    }

    data = {"filename": filename, "new_eval_phase": eval_phase}

    response = requests.put(
        url, headers=headers, json=data, auth=HTTPBasicAuth(PUBLIC_KEY, PRIVATE_KEY)
    )

    if response.status_code == 200:
        return True
    else:
        return False
