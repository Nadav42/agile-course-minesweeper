# Minesweeper
multiplayer minesweeper app made with Flask, React and Socket.IO

## Run tests
`python -m unittest discover ./tests`

or

`pip install pytest && pytest ./tests`

## Running with docker:
**Build Locally:**

`docker build -t minesweeper .`

`docker run -it --rm -p 5000:5000 minesweeper`

**From dockerhub.com:**

`docker run -it --rm -p 5000:5000 nadav42/minesweeper`

**Run with docker-compose**

`docker-compose -f ".../docker-compose-minesweeper-prod.yml" up -d`