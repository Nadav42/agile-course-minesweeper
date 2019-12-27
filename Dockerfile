# ----- first build the react app ----- #
FROM node:12.2.0-alpine as react-builder

WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY ./react/package.json /app/package.json

RUN npm install --silent
RUN npm install react-scripts@3.0.1 -g --silent

COPY ./react/src /app/src
COPY ./react/public /app/public

# for builds use RUN, not CMD!
RUN npm run build

# ----- then setup the flask server ----- #
FROM python:3.7.3-alpine3.10

# We copy just the requirements.txt first to leverage Docker cache (?????)
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

# install build dependencies like gcc then install pip requirements
# if no need for special build dependencies just --> RUN pip install -r requirements.txt
RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies

# copy python source code
COPY . /app

# clean react source folder from previous copy because we only need the build folder
RUN rm -rf /app/react

# copy build folder from docker react build stage
COPY --from=react-builder /app/build/ /app/react/build/

ENTRYPOINT [ "python" ]

CMD [ "flask_app.py" ]