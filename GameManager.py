from Minesweeper.Board import Board, GAME_NOT_FINISHED, GAME_WON, GAME_LOST, MIN_DIFFICULTY, MAX_DIFFICULTY

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

        return {"board": self.board.to_json(), "won": won, "finished": finished, "difficulty": self.board.get_difficulty()}

    def click(self, row, col):
        self.board.click(row, col)

    def flag_click(self, row, col):
        self.board.flag_click(row, col)

    def reset_game(self, rows=9, cols=9, mine_probability=0.13):
        self.board.reset(rows, cols, mine_probability)

    def get_difficulty_options(self):
        return {"min": MIN_DIFFICULTY, "max": MAX_DIFFICULTY}