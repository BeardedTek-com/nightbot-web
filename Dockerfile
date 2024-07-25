FROM python:3.10.14
RUN mkdir -p /flask/data
WORKDIR /flask
COPY . .
RUN python -m venv venv
RUN source venv/bin/activate && pip install -r requirements.txt
CMD flask run