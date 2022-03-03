from mein import TypingProgram


class TypingGame(TypingProgram):
    def __init__(self):
        super().__init__()

    def startGame(self):
        TypingGame.putToScreen(self, "something", self.middle_row, self.middle_col, napm=True)

if __name__ == "__main__":
    TypingGame()
