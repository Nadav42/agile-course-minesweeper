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

    def click(self, row, col):
        self.board.click(row, col)

    def flag_click(self, row, col):
        self.board.flag_click(row, col)

    def reset_game(self, rows=9, cols=9, mine_probability=0.13):
        self.board.reset(rows, cols, mine_probability)

    # return to user something like
    # {board: gameManager.get_board(), gameStatus: gameManager.game_status()}
