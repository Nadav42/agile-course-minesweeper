# ----- first build the react app ----- #
FROM node:12.2.0-alpine as react-builder

WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY ./react/package.json /app/package.json

RUN npm install && npm install react-scripts@3.0.1 -g && npm cache clean --force

COPY ./react/src /app/src
COPY ./react/public /app/public

# for builds use RUN, not CMD!
RUN npm run build

# ----- then install and start the flask server ----- #
FROM python:3.7.3-alpine3.10

WORKDIR /app

# install build dependencies like gcc then install pip requirements
RUN apk add --no-cache gcc musl-dev linux-headers

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

# copy python source code
COPY . /app

# clean react source folder from previous copy because we only need the build folder
RUN rm -rf /app/react

# copy build folder from docker react build stage
COPY --from=react-builder /app/build/ /app/react/build/

EXPOSE 5000

CMD ["python", "-u", "/app/flask_app.py"]