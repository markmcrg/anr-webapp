import streamlit as st
import streamlit_antd_components as sac
import hydralit_components as hc

def application_requirements():
    st.markdown("<h1 style='text-align: center;'>Application Requirements</h1>", unsafe_allow_html=True)

    

    
    cols = st.columns([0.4,1,0.4])
    with cols[1]:
        with st.container():
            accre_type = sac.segmented(
                items=[
                    sac.SegmentedItem(label='Accreditation'),
                    sac.SegmentedItem(label='Revalidation'),
                ],  align='center', radius='xl', divider=True, use_container_width=True, color='#800000'
            )

    if accre_type == "Accreditation":
        st.markdown("""
                        <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
                        <style>
                            #root {
                                background: red;
                            }
                            .st-emotion-cache-4uzi61 e1f1d6gn0 {
                                background: #f2a642;
                            }
                            h1 {
                                font-family: "Source Sans Pro", sans-serif;
                                font-weight: 700;
                                color: #f5c472;
                                padding: 1.25rem 0px 1rem;
                                margin: 0px;
                                line-height: 1.2;
                            }
                            .table {
                                background-color: #800000;
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
                                background-color: white !important;
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
                            a:link {
                                color: white;
                            }
                            a:visited {
                                color: white;
                            }
                            a:hover {
                                text-decoration: none;
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
                                            <li>Gender Sensitivity Orientation Certificate of Registration</li>
                                        </ul>
                                    </td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:w:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EQ9rND2NFPxEl66JLMDOZmoBGbeCyRoqhCRF9DzaKdY6cQ?e=8eeyIC" role="button">View</a></td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:b:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EUxfYewOexNGkB4ZJ6r_lzABYKKE-9GyNj5ANPBmPrfxZQ?e=bUjJPg" role="button">View</a></td>
                                </tr>
                                <tr>
                                    <td class="text-center">AD002</td>
                                    <td>Officers' Profile with 1st Semester Certificate of Registration, and list of members (at least 15 members including the officers/executives)</td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:w:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EegksUKC43BLtrHZGU5G_10BI7VetrRSQhJfkelz4p47tQ?e=NPbGCg" role="button">View</a></td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:b:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EdQ5xkt-LUFGuFr2PmHMvvkB6nW-Ic1J9_6tOsl6ONBR9A?e=gDibMb" role="button">View</a></td>
                                </tr>
                                <tr>
                                    <td class="text-center">AD003</td>
                                    <td>Adviser(s)'s Letter of Concurrence with scanned copy of their university-issued ID</td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:w:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EW0joq8X68dCsvjuPhFu5b4BWOk0MFyACDk9AGeld_g6Lw?e=deCHPa" role="button">View</a></td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:b:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EbyDnOfThgFKm05yWDtngAABQ5YRGwALMBK1hqkigEEy6A?e=nWbgfb" role="button">View</a></td>
                                </tr>
                                <tr>
                                    <td class="text-center">AD004</td>
                                    <td>Student Organization's Constitution and Bylaws (CBL)</td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:w:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/ESFCFFpqG2ZFsucRRk5y5_sByPc--ZIwLhZ2u1-bdnsAnA?e=T0jYjk" role="button">View</a></td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:b:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EX1ZUDu5BnVCthH0e_DmH50BVpW8t2pB_kASWhojVh-opQ?e=EopvHl" role="button">View</a></td>
                                </tr>
                                <tr>
                                    <td class="text-center">AD005</td>
                                    <td>General Plan of Activities with Budgetary Outlay</td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href=https://pupedu-my.sharepoint.com/:w:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EeRCR8D01ehJgTy1Fzpbn40B2FhQuqDFVIsVWY_sW1Gw9Q?e=rvnJX1" role="button">View</a></td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:b:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EVuQRQHVC1RLhwTTAo3jcxEBvLZEvKC8Owa_wrsGqcyLuA?e=Snm1c8" role="button">View</a></td>
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
                                color: #f5c472;
                                padding: 1.25rem 0px 1rem;
                                margin: 0px;
                                line-height: 1.2;
                            }
                            .table {
                                background-color: #800000;
                                border-radius: 15px;
                                box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                                overflow: hidden;
                                margin-bottom: 0;
                            }
                            .table th {
                                background-color: #800000 !important;
                                color: white;
                                vertical-align: middle;
                            }
                            .table td {
                                vertical-align: middle;
                                background-color: white !important;
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
                            a:link {
                                color: white;
                            }
                            a:visited {
                                color: white;
                            }
                            a:hover {
                                text-decoration: none;
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
                                            <li>Gender Sensitivity Orientation Certificate of Registration</li>
                                            <li>Scanned Copy of the Latest Certificate of Accreditation/Revalidation</li>
                                        </ul>
                                    </td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:w:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/ETn_YEA1qrxBjmmjvuop900BD_PA9D60Me2aZGyrx-B-yg?e=1enbFy" role="button">View</a></td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:b:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EbE3p4-lRJNAk8JMmccSsD8BWrc0AoT2mpFlnWjqfKORVA?e=boYLDR" role="button">View</a></td>
                                </tr>
                                <tr>
                                    <td class="text-center">RD002</td>
                                    <td>Officers' Profile with 1st Semester Certificate of Registration, and list of members (at least 15 members including the officers/executives)</td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:w:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/Ec2MYXQXxqFFtAVzUNpvyO0BgE71fNmeKQR3_Fa1E5u8qQ?e=ZLfRXb" role="button">View</a></td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:b:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/ESXVmJrKZDpPlSMH1oPbnx0BP45sQZ7FfBlq8edpKAEaAw?e=NgxF7z" role="button">View</a></td>
                                </tr>
                                <tr>
                                    <td class="text-center">RD003</td>
                                    <td>Adviser(s)'s Letter of Concurrence with scanned copy of their university-issued ID</td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:w:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EeEtEvl9PvRHt8cs4qX8EFIBGi7kcfFsDxIkEbfYWBiqDA?e=UA3QVb" role="button">View</a></td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:b:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EV4K_DuMSQdJoZBpkXiPaykBlHi7FqvX0i6AV56MUGA4Rg?e=kwHrhF" role="button">View</a></td>
                                </tr>
                                <tr>
                                    <td class="text-center">RD004</td>
                                    <td>Student Organization's Constitution and Bylaws (CBL)</td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:w:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EdlgiRVBUfNLmEvjYPDeNmUBTP6G7l2MGI5ooDXDL060xg?e=ZEqYFU" role="button">View</a></td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon disabled" href="" role="button">View</a></td>
                                </tr>
                                <tr>
                                    <td class="text-center">RD005</td>
                                    <td>General Plan of Activities with Budgetary Outlay</td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:w:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/Eco7-ObgpuZAs_U9zJPeaKcB7XRrjNUzBqLImM2ZxWrVqQ?e=Dmo3EH" role="button">View</a></td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:b:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EfHK1ndgvR1LhaPKlbdMJO8B_EIdHfTW_d3cXU4Jh3AAGQ?e=1bykTv" role="button">View</a></td>
                                </tr>
                                <tr>
                                    <td class="text-center">RD006</td>
                                    <td>Accomplishment Report (or substitute)</td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:w:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EZyAdDx-amFCh-iv4OCr8pgBNnLs0mx7hZv2B9nJqrThVQ?e=p0tc6Z" role="button">View</a></td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:b:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/ESpJDRr_N6hOmKgJ4zz58YQBBI41Gq9Vzvc3PAhFBsX8sw?e=HRD6je" role="button">View</a></td>
                                </tr>
                                <tr>
                                    <td class="text-center">RD007</td>
                                    <td>Copy of Approved Financial Statements</td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon disabled" href="" role="button">View</a></td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon disabled" href="" role="button">View</a></td>
                                </tr>
                                <tr>
                                    <td class="text-center">RD008</td>
                                    <td>Turnover of Assets and Funds</td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:w:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/EWcbmOn2PuJNi2lp-o4MAZkBH4QInQon6BZMIaumrRFxjg?e=lG3Fdm" role="button">View</a></td>
                                    <td class="text-center"><a class="btn btn-sm btn-maroon" href="https://pupedu-my.sharepoint.com/:b:/g/personal/cosoa_iskolarngbayan_pup_edu_ph/Eby2ekiqnHhOrBDZxGB-fhgBwDh7-BA2W95DjFr3eR65VA?e=eHMsNY" role="button">View</a></td>
                                </tr>
                            </tbody>
                        </table>
                    """, unsafe_allow_html=True)