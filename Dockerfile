FROM python:3.8-slim 

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN python3 -m ensurepip --default-pip
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt 

RUN apt-get update -y && apt-get install curl gnupg -y
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list 
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - 
RUN apt-get update -y && apt-get install google-cloud-sdk -y
       

CMD exec python3 cloudworker.py