from board import Board, GameOver


class Game:
    SYMBOLS = ['x', 'o']

    def __init__(self):
        self._player_char = None
        self._computer_char = None
        self._board = None
        self._player_first = None

    def start_new_game(self):
        """
        Initialization of the game.
        """
        print('Tic-Tac-Toe!')
        self._player_first = input("Choose your turn (1/2): "
                                   ).strip().upper() == '1'
        self._player_char = self.SYMBOLS[not self._player_first]
        print('Your symbol is: {}'.format(self._player_char))
        self._computer_char = self.SYMBOLS[self._player_first]
        self._board = Board()

    def _check_player_move(self):
        """
        Check if input is valid.
        """
        try:
            player_move = int(input('Enter a number of cell: '))
            assert player_move in self._board.free_cells
            return player_move
        except AssertionError:
            print('You can`t choose this cell.')
            return self._check_player_move()

    def _show_board(self):
        """
        Visualize the board.
        """
        board_str = str(self._board).replace('True', self._computer_char). \
            replace('False', self._player_char)
        print(board_str)

    def run(self):
        """
        Running the game.
        """
        self._show_board()
        if self._player_first:
            self._board.player_move(self._check_player_move())
            self._show_board()
            print("  ---------")
        try:
            while True:
                self._board.computer_move()
                self._show_board()
                self._board.player_move(self._check_player_move())
                self._show_board()
                print("  ---------")
        except GameOver as err:
            self._show_board()
            self.game_finish(str(err))

    def game_finish(self, end):
        if end == 'Computer won!':
            print('You lost!')
        elif end == 'Player won!':
            print('You won!')
        else:
            print(end)


def main():
    game = Game()
    game.start_new_game()
    game.run()

if __name__ == "__main__":
    main()
