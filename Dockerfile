FROM python:3.7.3-alpine3.10

# We copy just the requirements.txt first to leverage Docker cache (?????)
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

# install build dependencies like gcc then install pip requirements
RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies

# if no need for special build dependencies
# RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "flask_app.py" ]