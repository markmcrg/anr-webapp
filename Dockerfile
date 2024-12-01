FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    ssh \
    git \
    && rm -rf /var/lib/apt/lists/*


# Define ARGs for environment variables
ARG b2_applicationKey
ARG b2_keyID
ARG b2_keyName
ARG db1_database
ARG db1_host
ARG db1_password
ARG db1_port
ARG db1_user
ARG db2_database
ARG db2_host
ARG db2_password
ARG db2_port
ARG db2_user
ARG mt_notif_template_uuid
ARG mt_otp_template_uuid
ARG mt_token
ARG tidb_private_key
ARG tidb_public_key

# Add a dummy build argument to bust cache
RUN echo "Cache bust: ${KOYEB_GIT_SHA}"

# Clone the private repository using a GitHub PAT
ARG GIT_TOKEN
RUN git clone https://$GIT_TOKEN@github.com/markmcrg/anr-webapp.git . 

RUN pip3 install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py"]