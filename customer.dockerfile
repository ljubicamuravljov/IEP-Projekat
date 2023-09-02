
FROM python:3

RUN mkdir -p /opt/src/shopApp
WORKDIR /opt/src/shopApp

COPY shopApp/customerApp.py ./customerApp.py
COPY shopApp/configuration.py ./configuration.py
COPY shopApp/models.py ./models.py
COPY shopApp/decorator.py ./decorator.py
COPY shopApp/requirements.txt ./requirements.txt
COPY shopApp/Order.abi ./Order.abi
COPY shopApp/Order.bin ./Order.bin
COPY shopApp/bcThings.py ./bcThings.py

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/shopApp"

#ENTRYPOINT ["echo","hello world"]
#ENTRYPOINT ["sleep","1200"]

ENTRYPOINT ["python", "./customerApp.py"]
