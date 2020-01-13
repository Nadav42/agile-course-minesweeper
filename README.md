# Minesweeper
multiplayer minesweeper app made with Flask, React and Socket.IO

## Install from source code
1. install all dependencies

    `pip install -r requirements.txt`

2. run the app

    `python flask_app.py`

3.  open http://localhost:5000/

## Run tests
`python -m unittest discover ./tests`

or

`pip install pytest && pytest ./tests`

## Run with docker:
**Build Locally:**

`docker build -t minesweeper .`

`docker run -it --rm -p 5000:5000 minesweeper`

**Download image from dockerhub.com:**

`docker run -it --rm -p 5000:5000 nadav42/minesweeper`

**Run with docker-compose**

`docker-compose -f ".../docker-compose-minesweeper-prod.yml" up -d`