FROM python:3.10.14
RUN mkdir -p /flask/data
WORKDIR /flask
COPY . .
RUN python -m venv /data/venv
CMD /flask/start.sh