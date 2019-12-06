from Minesweeper.Board import Board, GAME_NOT_FINISHED, GAME_WON, GAME_LOST

class GameManager:

    def __init__(self):
        self.board = Board()

    def get_board_with_status(self):
        finished = False
        won = False
        if self.board.get_game_status() == GAME_WON:
            won = True
            finished = True
        if self.board.get_game_status() == GAME_LOST:
            finished =True

        return {"board": self.board.to_json(), "won": won, "finished": finished}

        # return self.board.to_json()

    # def game_status(self):
    #     return self.board.get_game_status() # GAME_NOT_FINISHED, GAME_WON, GAME_LOST

    def click(self, row, col):
        self.board.click(row, col)

    def flag_click(self, row, col):
        self.board.flag_click(row, col)

    def reset_game(self):
        self.board.reset()

    # return to user something like
    # {board: gameManager.get_board(), gameStatus: gameManager.game_status()}
