
# AnR Web App

The AnR Web App is a web application designed to facilitate and streamline the annual Accreditation and Revalidation Process at the Polytechnic University of the Philippines.

## Description
The AnR Web App aims to simplify the Accreditation and Revalidation Process by providing a centralized platform for users to view accredited organizations, submit applications, and check the status of their submissions. The app streamlines the entire process, making it more efficient and user-friendly.

## Installation
To set up the AnR Web App, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies using the provided `requirements.txt` file.
3. Set up the necessary environment variables for the TiDB Serverless MySQL database, Mailtrap for email sending, and BackBlaze B2 for file storage.
4. Run the Streamlit application to start the web app.

## Features

The AnR Web App offers the following key features:

### View Accredited Organizations
- Users can view a list of all organizations that have been accredited through the Accreditation and Revalidation Process.

### Access Application Requirements
- Users can access the detailed application requirements for the Accreditation and Revalidation Process directly through the web app.

### Submit Applications
- The web app allows users to submit their applications for the Accreditation and Revalidation Process directly through the platform.

### Track Application Status
- Users can check the status of their submitted applications, allowing them to stay up-to-date on the progress of their submissions.

## Technologies Used
The AnR Web App is built using the following technologies:

- **Streamlit**: A Python library for building interactive web applications.
- **TiDB Serverless**: A MySQL database service for storing user information and application data.
- **Mailtrap**: A service for testing and sending emails during the application process.
- **BackBlaze B2**: A cloud storage service for storing application files and documents.

## Site Link
The AnR Web App is hosted at [sccosoa.com](https://sccosoa.com).

## Developer Reference
- [Streamlit](https://docs.streamlit.io/develop/api-reference) 
- [Streamlit-antd-components](https://github.com/nicedouble/StreamlitAntdComponents) - [Demo App](https://nicedouble-streamlitantdcomponentsdemo-app-middmy.streamlit.app/)
- [Mailtrap](https://api-docs.mailtrap.io/) - [Python SDK](https://github.com/railsware/mailtrap-python)
- [Backblaze B2 Native API](https://www.backblaze.com/docs/cloud-storage-native-api) - [Python SDK](https://b2-sdk-python.readthedocs.io/en/master/api_reference.html)
- [Backblaze B2 API Call Pricing](https://www.backblaze.com/cloud-storage/transaction-pricing)
