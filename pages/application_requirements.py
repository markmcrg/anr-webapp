import streamlit as st
import streamlit_antd_components as sac

def application_requirements():
    st.markdown("<h1 style='text-align: center;'>Application Requirements</h1>", unsafe_allow_html=True)

    cols = st.columns([0.4,1,0.4])


    with cols[1]:
        accre_type = sac.segmented(
            items=[
                sac.SegmentedItem(label='Accreditation'),
                sac.SegmentedItem(label='Revalidation'),
            ],  align='center', radius='xl', divider=True, use_container_width=True,
        )

    if accre_type == "Accreditation":
        st.markdown("""
                        <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
                        <style>
                            h1 {
                                font-family: "Source Sans Pro", sans-serif;
                                font-weight: 700;
                                color: rgb(49, 51, 63);
                                padding: 1.25rem 0px 1rem;
                                margin: 0px;
                                line-height: 1.2;
                            }
                            .table {
                                background-color: white;
                                border-radius: 15px;
                                box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                                overflow: hidden;
                                margin-bottom: 0;
                            }
                            .table th {
                                background-color: #800000;
                                color: white;
                                vertical-align: middle;
                            }
                            .table td {
                                vertical-align: middle;
                            }
                            .table ul {
                                margin-bottom: -5px;
                            }
                            .table-striped tbody tr:nth-of-type(odd) {
                                background-color: rgba(128, 0, 0, 0.05);
                            }
                            .btn-maroon {
                                background-color: #800000;
                                border-color: #800000;
                                color: white;
                            }
                            .btn-maroon:hover {
                                background-color: #600000;
                                border-color: #600000;
                                color: white;
                            }
                            .text-center {
                                text-align: center;
                            }
                            
                            .table tbody tr:last-child td {
                                border-bottom: none;
                            }
                        </style>
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th class="text-center">Form Code</th>
                                    <th>Requirement</th>
                                    <th class="text-center">Template</th>
                                    <th class="text-center">Sample</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td class="text-center">AD001</td>
                                    <td>Compilation of Compulsory Certificates
                                        <ul>
                                            <li>Certificate of Recognition from Central/Local Student Council</li>
                                            <li>Certificate of Clearance from PUP Student Council Commission on Audit (PUP SC COA)</li>
                                            <li>OSS Anti-Hazing Orientation Certificate of Registration</li>
                                        </ul>
                                    </td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                </tr>
                                <tr>
                                    <td class="text-center">AD002</td>
                                    <td>Officers' Profile with 1st Semester Certificate of Registration, and list of members (at least 15 members including the officers/executives)</td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                </tr>
                                <tr>
                                    <td class="text-center">AD003</td>
                                    <td>Adviser(s)'s Letter of Concurrence with scanned copy of their university-issued ID</td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                </tr>
                                <tr>
                                    <td class="text-center">AD004</td>
                                    <td>Student Organization's Constitution and Bylaws (CBL)</td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                </tr>
                                <tr>
                                    <td class="text-center">AD005</td>
                                    <td>General Plan of Activities with Budgetary Outlay</td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                </tr>
                            </tbody>
                        </table>
                    """, unsafe_allow_html=True)

        
    elif accre_type == "Revalidation":
         st.markdown("""
                        <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
                        <style>
                            h1 {
                                font-family: "Source Sans Pro", sans-serif;
                                font-weight: 700;
                                color: rgb(49, 51, 63);
                                padding: 1.25rem 0px 1rem;
                                margin: 0px;
                                line-height: 1.2;
                            }
                            .table {
                                background-color: white;
                                border-radius: 15px;
                                box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                                overflow: hidden;
                                margin-bottom: 0;
                            }
                            .table th {
                                background-color: #800000;
                                color: white;
                                vertical-align: middle;
                            }
                            .table td {
                                vertical-align: middle;
                            }
                            .table ul {
                                margin-bottom: -5px;
                            }
                            .table-striped tbody tr:nth-of-type(odd) {
                                background-color: rgba(128, 0, 0, 0.05);
                            }
                            .btn-maroon {
                                background-color: #800000;
                                border-color: #800000;
                                color: white;
                            }
                            .btn-maroon:hover {
                                background-color: #600000;
                                border-color: #600000;
                                color: white;
                            }
                            .text-center {
                                text-align: center;
                            }
                            
                            .table tbody tr:last-child td {
                                border-bottom: none;
                            }
                        </style>
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th class="text-center">Form Code</th>
                                    <th>Requirement</th>
                                    <th class="text-center">Template</th>
                                    <th class="text-center">Sample</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td class="text-center">RD001</td>
                                    <td>Compilation of Compulsory Certificates
                                        <ul>
                                            <li>Certificate of Recognition from Central/Local Student Council</li>
                                            <li>Certificate of Clearance from PUP Student Council Commission on Audit (PUP SC COA)</li>
                                            <li>OSS Anti-Hazing Orientation Certificate of Registration</li>
                                            <li>Scanned Copy of the Latest Certificate of Accreditation/Revalidation</li>
                                        </ul>
                                    </td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                </tr>
                                <tr>
                                    <td class="text-center">RD002</td>
                                    <td>Officers' Profile with 1st Semester Certificate of Registration, and list of members (at least 15 members including the officers/executives)</td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                </tr>
                                <tr>
                                    <td class="text-center">RD003</td>
                                    <td>Adviser(s)'s Letter of Concurrence with scanned copy of their university-issued ID</td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                </tr>
                                <tr>
                                    <td class="text-center">RD004</td>
                                    <td>Student Organization's Constitution and Bylaws (CBL)</td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                </tr>
                                <tr>
                                    <td class="text-center">RD005</td>
                                    <td>General Plan of Activities with Budgetary Outlay</td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                </tr>
                                <tr>
                                    <td class="text-center">RD006</td>
                                    <td>Accomplishment Report (or substitute)</td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                </tr>
                                <tr>
                                    <td class="text-center">RD007</td>
                                    <td>Copy of Approved Financial Statements</td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                </tr>
                                <tr>
                                    <td class="text-center">RD008</td>
                                    <td>Turnover of Assets and Funds</td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                    <td class="text-center"><button class="btn btn-sm btn-maroon">View</button></td>
                                </tr>
                            </tbody>
                        </table>
                    """, unsafe_allow_html=True)