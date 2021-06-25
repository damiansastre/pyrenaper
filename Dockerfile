FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y python3.9
WORKDIR /app
COPY . /app
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt
CMD ["encoder.py"]
ENTRYPOINT ["python3"]

