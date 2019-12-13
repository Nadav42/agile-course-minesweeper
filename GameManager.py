import hashlib

from Minesweeper.Board import Board, GAME_NOT_FINISHED, GAME_WON, GAME_LOST, MIN_DIFFICULTY, MAX_DIFFICULTY

def md5(value):
    m = hashlib.md5()
    m.update(str(value).encode('utf-8'))
    return m.hexdigest()

class Lobby:

    lobby_generated_id = 1

    def __init__(self, lobby_name, password=None):
        self.lobby_name = lobby_name
        self.lobby_key = md5(Lobby.lobby_generated_id)

        # encrypt password if not none (TODO: md5 is not safe for passwords, change this in the future)
        if password is not None:
            password = md5(password)

        # store only encrypted password
        self.password_encrypted = password

        self.board = Board()

        # next id
        Lobby.lobby_generated_id = Lobby.lobby_generated_id + 1

    def get_lobby_key(self):
        return self.lobby_key

    def get_board(self):
        return self.board

    def has_password(self):
        return (self.password_encrypted is not None)

    # TODO: change from md5 to more secure hash
    def check_password_correct(self, password):
        return (md5(password) == self.password_encrypted)

    def to_json(self):
        return {"key": self.lobby_key, "name": self.lobby_name, "hasPassword": (self.password_encrypted is not None)}

class GameManager:

    def __init__(self):
        self.lobbies = {}

        self.create_lobby("Demo Lobby3", password="1234")
        self.create_lobby("Demo Lobby2")
        self.create_lobby("Demo Lobby1")

    def get_board_with_status(self, lobby_key):
        board = self.get_lobby(lobby_key).get_board()

        finished = False
        won = False
        if board.get_game_status() == GAME_WON:
            won = True
            finished = True
        if board.get_game_status() == GAME_LOST:
            finished =True

        return {"board": board.to_json(), "won": won, "finished": finished, "difficulty": board.get_difficulty()}

    def click(self, lobby_key, row, col):
        board = self.get_lobby(lobby_key).get_board()
        board.click(row, col)

    def flag_click(self, lobby_key, row, col):
        board = self.get_lobby(lobby_key).get_board()
        board.flag_click(row, col)

    def reset_game(self, lobby_key, rows=9, cols=9, mine_probability=0.13):
        board = self.get_lobby(lobby_key).get_board()
        board.reset(rows, cols, mine_probability)

    def get_difficulty_options(self):
        return {"min": MIN_DIFFICULTY, "max": MAX_DIFFICULTY}

    # ----- lobbies ----- #

    def create_lobby(self, lobby_name, password=None):
        lobby = Lobby(lobby_name, password=password)
        lobby_key = lobby.get_lobby_key()

        # lobby key is auto generated
        self.lobbies[lobby_key] = lobby

        return lobby_key

    def get_lobby(self, lobby_key):
        if lobby_key in self.lobbies:
            return self.lobbies[lobby_key]

        return None

    def get_lobbies_list(self):
        lobbies_list = []

        for key in self.lobbies:
            lobbies_list.append(self.lobbies[key].to_json())

        return lobbies_list
