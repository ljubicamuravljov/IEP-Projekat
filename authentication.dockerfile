
FROM python:3

RUN mkdir -p /opt/src/authentication
WORKDIR /opt/src/authentication

COPY authentication/configuration.py ./configuration.py
COPY authentication/application.py ./application.py
COPY authentication/models.py ./models.py
COPY authentication/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH = "/opt/src/authentication"

#ENTRYPOINT ["echo","hello world"]
#ENTRYPOINT ["sleep","1200"]

ENTRYPOINT ["python","./application.py"]