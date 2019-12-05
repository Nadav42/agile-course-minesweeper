from Minesweeper.Board import Board, GAME_NOT_FINISHED, GAME_WON, GAME_LOST

class GameManager:

    def __init__(self):
        self.board = Board()

    def get_board(self):
        return self.board.to_json()

    def game_status(self):
        return self.board.get_game_status() # GAME_NOT_FINISHED, GAME_WON, GAME_LOST

    def click(self, row, col):
        self.board.click(row, col)

    def flag_click(self, row, col):
        self.board.flag_click(row, col)

    def reset_game(self):
        self.board.reset()

    # return to user something like
    # {board: gameManager.get_board(), gameStatus: gameManager.game_status()}
