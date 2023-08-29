
FROM python:3

RUN mkdir -p /opt/src/shopApp
WORKDIR /opt/src/shopApp

COPY shopApp/courierApp.py ./courierApp.py
COPY shopApp/configuration.py ./configuration.py
COPY shopApp/models.py ./models.py
COPY shopApp/decorator.py ./decorator.py
COPY shopApp/requirements.txt ./requirements.txt
#COPY eth/order.abi ./order.abi
#COPY eth/order.bin ./order.bin

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/shopApp"

#ENTRYPOINT ["echo","hello world"]
#ENTRYPOINT ["sleep","1200"]

ENTRYPOINT ["python", "./courierApp.py"]
