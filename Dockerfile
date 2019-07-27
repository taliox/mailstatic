FROM python:3.6
ENV PYTHONUNBUFFERED 1
#RUN mkdir /opt/webapp
WORKDIR /opt/webapp
ADD requirements.txt /opt/webapp
RUN pip install -r requirements.txt