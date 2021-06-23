FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y -q openjdk-8-jdk
RUN apt-get install -y python3.9
RUN apt-get install -y libzbar-dev zbar-tools python3-opencv
WORKDIR /app
COPY . /app
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt
CMD ["encoder.py"]
ENTRYPOINT ["python3"]

