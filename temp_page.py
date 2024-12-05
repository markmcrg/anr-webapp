import streamlit as st
st.set_page_config("under maintenance :(", page_icon="logo.png", layout="wide")
# Custom CSS for styling
st.markdown("""
    <style>
        body {
            font-family: arial, sans-serif;
            background-color: #800000;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            text-align: center;
        }
        .container {
            max-width: 600px;
            padding: 15px;
        }
        .logo {
            width: 150px;
            height: 150px;
            margin: 0 auto 30px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .logo img {
            max-width: 100%;
            max-height: 100%;
            border-radius: 50%;
        }
        h1 {
            font-size: 36px;
            margin-bottom: 20px;
            color: #ffffff;
        }
        p {
            font-size: 18px;
            line-height: 1.6;
            color: #ffffff;
        }
    </style>
    """, unsafe_allow_html=True)

# HTML structure using Streamlit components
page_bg_img = f"""
<style>
#root > div:nth-child(1) > div.withScreencast > div > div{{
background-color: #800000;
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
</style>
"""
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown('<div class="logo"><img src="https://i.imgur.com/5OAGTVj.png" alt="PUP SC COSOA"></div>', unsafe_allow_html=True)  # Replace with your logo path
st.markdown('<h1>under maintenance :(</h1>', unsafe_allow_html=True)
st.markdown("<p>we're trying to be back asap. <a href='https://forms.office.com/r/fNhQfxJXUL' style='color: inherit; text-decoration: underline;'>join our discord to stay updated!</a> </p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
# sample texts: we're working hard to bring you something amazing.
# we should be back soon.
