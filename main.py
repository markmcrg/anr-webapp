import streamlit as st
import streamlit_antd_components as sac
import pages as pg
from helpers import get_role, get_abbreviation, update_last_login
import streamlit_shadcn_ui as ui
from streamlit_tailwind import st_tw
import hydralit_components as hc
import time

# Entrypoint / page router for the app
st.set_page_config(page_title="PUP SC COSOA AnR Portal", page_icon="page_logo.png", layout="wide")
st.logo('logo.png', link='https://www.sccosoa.com', icon_image='logo.png', size='large') # Change link to sccosoa.com in production

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'name' not in st.session_state:
    st.session_state['name'] = None

loader_index = 5
override_theme = ""
with st.sidebar:
    if st.session_state["authentication_status"] is None or not st.session_state["authentication_status"] :
        menu_item = sac.menu([
            sac.MenuItem('Guest Menu', disabled=True),
            sac.MenuItem(type='divider'),
            sac.MenuItem('Home', icon='bi bi-house-door'),
            sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
            sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
            sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),
            sac.MenuItem('Sign Up', icon='bi bi-person-plus'),
            sac.MenuItem('Login', icon='bi bi-box-arrow-in-right'),
            sac.MenuItem('Password Reset', icon='bi bi-key'),
        ], open_all=False, index=2, size ='md',)
    
    if st.session_state["authentication_status"]:
        role = get_role(st.session_state["username"])
        if role == 'cosoa':
            abbreviation = get_abbreviation(st.session_state["username"])
            menu_item = sac.menu([
                sac.MenuItem(f'Welcome, {str(abbreviation)}!', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Home', icon='bi bi-house-door'),
                sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
                sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
                sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),
                sac.MenuItem('Evaluate Submissions', icon='bi bi-file-earmark-text'),
                sac.MenuItem('Account Settings', icon='bi bi-person-gear'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-in-left'),
            ], open_all=False, index=2)
        elif role == 'user':
            abbreviation = get_abbreviation(st.session_state["username"])
            menu_item = sac.menu([
                sac.MenuItem(f'Welcome, {str(abbreviation)}!', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Home', icon='bi bi-house-door'),
                sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
                sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
                sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),
                sac.MenuItem('Accreditation Application', icon='bi bi-file-earmark-text'),
                sac.MenuItem('Accreditation Status', icon='bi bi-graph-up-arrow'),
                sac.MenuItem('Account Settings', icon='bi bi-person-gear'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-in-left'),
            ], open_all=False, index=2)
        elif role == 'chair':
            menu_item = sac.menu([
                sac.MenuItem('Welcome, Chair!', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Home', icon='bi bi-house-door'),
                sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
                sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
                sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),
                sac.MenuItem('Evaluate Submissions', icon='bi bi-clipboard-check'),
                sac.MenuItem('Account Settings', icon='bi bi-person-gear'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-in-left'),
                
                sac.MenuItem("", disabled=True),
                
                sac.MenuItem('Admin Tools', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Assign Organizations', icon='bi bi-person-check'),
                sac.MenuItem("User Management", icon='bi bi-person-lines-fill'),
                sac.MenuItem("Metrics", icon='bi bi-graph-up-arrow'),
                sac.MenuItem('View Document Status', icon='bi bi-file-earmark-text'),
            ], open_all=False, index=2)
        elif role == 'execcomm':
            abbreviation = get_abbreviation(st.session_state["username"])
            menu_item = sac.menu([
                sac.MenuItem(f'Welcome, {str(abbreviation)}!', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Home', icon='bi bi-house-door'),
                sac.MenuItem('Accredited Organizations', icon='bi bi-building'),
                sac.MenuItem('Application Requirements', icon='bi bi-clipboard-check'),
                sac.MenuItem('Frequently Asked Questions', icon='bi bi-question-circle'),
                sac.MenuItem('Evaluate Submissions', icon='bi bi-clipboard-check'),
                sac.MenuItem('Account Settings', icon='bi bi-person-gear'),
                sac.MenuItem('Logout', icon='bi bi-box-arrow-in-left'),
                
                sac.MenuItem("", disabled=True),

                sac.MenuItem('Admin Tools', disabled=True),
                sac.MenuItem(type='divider'),
                sac.MenuItem('Assign Organizations', icon='bi bi-person-check'),
                sac.MenuItem('View Document Status', icon='bi bi-file-earmark-text'),
            ], open_all=False)
    page_bg_img = """
    <style>
        [data-testid="stAppViewContainer"] {
        background-image: url("https://i.imgur.com/uwxp9Br.png");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: local;
        }
        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }
        input {
            background-color: #F0F2F6 !important;
        }
        .st-emotion-cache-4uzi61 e1f1d6gn0 {
            background-color: red !important;
        }
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stMain.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stMainBlockContainer.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div.stHorizontalBlock.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.stColumn.st-emotion-cache-949r0i.e1f1d6gn3 > div > div > div > div > div > div > div > iframe {
            border-radius: 25px
        }
        #root > ul {
            font-family: 'Source Sans Pro', sans-serif !important; 
        }
        h1 {
            text-shadow: 2px 4px 6px #2e2c2c;
            color: #f5c472 !important;
        }

    </style>
"""
    st.markdown(page_bg_img, unsafe_allow_html=True)

if menu_item == 'Home':
    pg.home()
if menu_item == 'Accredited Organizations': 
    with hc.HyLoader('',hc.Loaders.standard_loaders,index=[loader_index]):
        pg.accredited_orgs()
elif menu_item == 'Application Requirements':
    pg.application_requirements()
elif menu_item == 'Frequently Asked Questions':
    pg.faqs()
elif menu_item == 'Sign Up':
    pg.signup()
elif menu_item == 'Login':
    with hc.HyLoader('',hc.Loaders.standard_loaders,index=[loader_index]):
        pg.login()
        if st.session_state["authentication_status"]:
            menu_item = 'Home'
            update_last_login(st.session_state["username"])
            st.rerun()
elif menu_item == 'Logout':
    pg.login(logout=True)
elif menu_item == 'Accreditation Application':
    # with hc.HyLoader('',hc.Loaders.standard_loaders,index=[loader_index]):
        pg.accreditation_application()
        
elif menu_item == 'Accreditation Status':
    pg.accreditation_status()
elif menu_item == 'User Management':
    pg.user_management()
elif menu_item == 'Account Settings':
    pg.account_settings()
elif menu_item == 'Password Reset':
    pg.forgot_password()
elif menu_item == "Assign Organizations":
    pg.assign_orgs()
elif menu_item == "Evaluate Submissions":
    pg.view_submissions() 
elif menu_item == "View Document Status":
    pg.document_management()

if st.session_state["authentication_status"]:
    menu_item = 'Home'
elif st.session_state["authentication_status"] is None or not st.session_state["authentication_status"]:
    pass

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
# user - for orgs
# cosoa - for evals
# execcomm - for org assignment
# chair - for admin level access (see all user info and change access levels)

# Inject custom CSS to style the div
st.markdown(
    """
    <style>
    .st-emotion-cache-4uzi61.e1f1d6gn0 {
    -webkit-text-size-adjust: 100%;
    tab-size: 4;
    font-family: ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,"Apple Color Emoji","Segoe UI Emoji",Segoe UI Symbol,"Noto Color Emoji";
    font-feature-settings: normal;
    font-variation-settings: normal;
    --background: 0 0% 100%;
    --foreground: 240 10% 3.9%;
    --card: 0 0% 100%;
    --card-foreground: 240 10% 3.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 240 10% 3.9%;
    --primary: 240 5.9% 10%;
    --primary-foreground: 0 0% 98%;
    --secondary: 240 4.8% 95.9%;
    --secondary-foreground: 240 5.9% 10%;
    --muted: 240 4.8% 95.9%;
    --muted-foreground: 240 3.8% 46.1%;
    --accent: 240 4.8% 95.9%;
    --accent-foreground: 240 5.9% 10%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;
    --border: 240 5.9% 90%;
    --input: 240 5.9% 90%;
    --ring: 240 10% 3.9%;
    --radius: .5rem;
    --primary-color: #8b0000;
    --background-color: #ffffff;
    --secondary-background-color: #f0f2f6;
    --text-color: #31333F;
    --font: "Source Sans Pro", sans-serif;
    line-height: inherit;
    box-sizing: border-box;
    border-style: solid;
    border-color: hsl(var(--border));
    --tw-border-spacing-x: 0;
    --tw-border-spacing-y: 0;
    --tw-translate-x: 0;
    --tw-translate-y: 0;
    --tw-rotate: 0;
    --tw-skew-x: 0;
    --tw-skew-y: 0;
    --tw-scale-x: 1;
    --tw-scale-y: 1;
    --tw-pan-x: ;
    --tw-pan-y: ;
    --tw-pinch-zoom: ;
    --tw-scroll-snap-strictness: proximity;
    --tw-gradient-from-position: ;
    --tw-gradient-via-position: ;
    --tw-gradient-to-position: ;
    --tw-ordinal: ;
    --tw-slashed-zero: ;
    --tw-numeric-figure: ;
    --tw-numeric-spacing: ;
    --tw-numeric-fraction: ;
    --tw-ring-inset: ;
    --tw-ring-offset-width: 0px;
    --tw-ring-offset-color: #fff;
    --tw-ring-color: rgb(59 130 246 / .5);
    --tw-ring-offset-shadow: 0 0 #0000;
    --tw-ring-shadow: 0 0 #0000;
    margin: .5rem;
    border-radius: .75rem;
    border-width: 1px;
    background-color: hsl(var(--card));
    color: hsl(var(--card-foreground));
    --tw-shadow: 0 1px 3px 0 rgb(0 0 0 / .1), 0 1px 2px -1px rgb(0 0 0 / .1);
    --tw-shadow-colored: 0 1px 3px 0 var(--tw-shadow-color), 0 1px 2px -1px var(--tw-shadow-color);
    box-shadow: var(--tw-ring-offset-shadow, 0 0 #0000),var(--tw-ring-shadow, 0 0 #0000),var(--tw-shadow);
    }
    .st-emotion-cache-1whx7iy e1nzilvr4 {
        color: red;
    }
    # [data-testid=stSidebar] {
    #     background-color: #6C2F3A !important;
    # }
    </style>
    """,
    unsafe_allow_html=True
)
# cols = st.columns([0.5, 1, 0.5])
# with cols[1]:
#     with st.container(border=True):
#         # value = st_tw(
#         #     text="""
#         #         <div class="text-gray-400 text-sm font-medium m-1">Email</div>
#         #     """, height=20
#         # )
#         st.markdown("### Login")
#         input_value = ui.input(type='text', placeholder="Email", key="input1")
#         input_value2 = ui.input(type='password', placeholder="Password", key="input2")
#         ui.button("Login", key="button1", className="m-1")

# value = st_tw(
#         text="""
#             <div class="bg-white p-4 h-48 rounded-lg">asd</div>
#         """,
#     )
# st.write(input_value)
# st.write(input_value2)
# st.write(value)
# st.write(test2.state)
# st.write(test3.state)


