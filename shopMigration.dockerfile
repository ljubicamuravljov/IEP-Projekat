FROM python:3

RUN mkdir -p /opt/src/shopApp
WORKDIR /opt/src/shopApp

COPY shopApp/migrate.py ./migrate.py
COPY shopApp/configuration.py ./configuration.py
COPY shopApp/models.py ./models.py
COPY shopApp/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt


#ENTRYPOINT ["echo","hello world"]
#ENTRYPOINT ["sleep","1200"]

ENTRYPOINT ["python","./migrate.py"]