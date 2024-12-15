import streamlit as st

def home():
    st.markdown("""
            <style>
            span {
                font-size: 18px;
                text-shadow: 2px 2px 6px #2e2c2c;
                line-height: 1.6;
                text-size-adjust: 100%;
                font-family: "Source Sans Pro", sans-serif;
                font-weight: 400;
                word-break: break-word;
                box-sizing: border-box;
                color: white;
            }
            p {
                text-align: justify;
            }
            [data-testid="stImageCaption"] {
                color: #e8e4c9;
                }
            #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stMain.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stMainBlockContainer.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div {
                margin-top: -90px;
            }
            #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stMain.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stMainBlockContainer.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div.stHorizontalBlock.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.stColumn.st-emotion-cache-1h4axjh.e1f1d6gn3 > div > div > div > div:nth-child(5) > div > div {
                margin-left: -90px;
            }
            </style>


            """
            ,unsafe_allow_html=True)


    cols = st.columns([0.01, 1, 0.01])
    with cols[1]:
        st.markdown("<h1 style='text-align: left; color: white;'>What is <span style='color: #f5c472; font-size:70px; font-weight: 700;'>COSOA</span>?</h1>", unsafe_allow_html=True)
        st.markdown("<span style='color: white;'>\
                        The Polytechnic University of the Philippines Student Council Commission on Student Organizations and Accreditation (PUP SC COSOA) serves as the sole-accrediting body and an independent student body set to develop an effective working relationship between the Central Student Council, the Office of Student Services (OSS), and all student organizations at the Polytechnic University of the Philippines, Sta. Mesa, Manila.\
                    </span>", 
                    unsafe_allow_html=True)
        st.markdown("<span style='color: white;'>\
                        At the core of the PUP SC COSOA's mission is a commitment to foster a streamlined and accessible accreditation and revalidation process, and to reduce the administrative burden for student organizations in attaining and maintaining their legal status. We aim to simplify the way organizations achieve their recognition, and enable them to focus better on their initiatives and contributions to the university community.\
                    </span>", 
                    unsafe_allow_html=True)
        st.image("https://i.imgur.com/y2rCqbk.jpeg", caption='PUP SC COSOA General Assembly 02 at the PUP COC Audio-Visual Room.', use_container_width=True)
        table_html = """
    <!-- Link to Bootstrap CSS and Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css" rel="stylesheet">

    <style>
    .custom-btn {
        background-color: #800000;
        color: #f5c472 !important;
        border: none;
        font-weight: bold; /* Make text bold */
        font-size: 1.15rem; /* Increase font size */
        padding: 9px 25px; /* Increase padding for larger buttons */
        border-radius: 30px; /* Optional: add border radius */
        text-decoration: none; /* Remove underline from links */
        display: inline-block; /* Ensure the anchor behaves like a button */
        margin-right: 10px; /* Space between buttons */
        box-shadow: 1px 1px 7px #2e2c2c;
    }
    .custom-btn:hover {
        background-color: #970000; /* Darker shade on hover */
        text-decoration: none; /* Remove underline from links */
    }
    .custom-btn:link {
        color: #f5c472 !important;
    }
    .custom-btn:active {
        background-color: #970000 !important;
        color: #f5c472 !important;
    }
    .icon-spacing {
        margin-right: 5px; /* Space between icon and text */
    }
    </style>



    <a href="https://www.facebook.com/pup.sccosoa" class="btn custom-btn" style="margin-left:15px;">
        <i class="bi bi-facebook icon-spacing"></i> Facebook
    </a>
    <!-- Email button as an anchor tag -->
    <a href="mailto:cosoa@iskolarngbayan.pup.edu.ph" class="btn custom-btn">
        <i class="bi bi-envelope-fill icon-spacing"></i> Email
    </a>
    """
    st.markdown(table_html, unsafe_allow_html=True)
    