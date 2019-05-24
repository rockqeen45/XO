import random
import copy



class Tree:
    def __init__(self, state, last_move):
        self._root = Tnode(state, last_move)

    def _next_states(self):
        """
        Finds all possible states from the root.
        """
        def recursive(current_node):
            current_node.points = current_node.analyse_state()
            if current_node.points == 0:
                for cell in current_node.free_cells:
                    next_state = copy.deepcopy(current_node.state)
                    next_move = (not current_node.last_move[0], cell)
                    i, j = Board.number_cell_to_state_indexes(cell)
                    next_state[i][j] = next_move[0]
                    new_node = Tnode(next_state, next_move)
                    current_node.next_states.append(new_node)
                    recursive(new_node)

                current_node.points = 0
                for next_node in current_node.next_states:
                    current_node.points += next_node.points
        recursive(self._root)

    def choose_next_move(self):
        """
        Finds best one state to continue a game.
        """
        self._next_states()
        if self._root.next_states:
            top_score = max(self._root.next_states).points
            best_states = []
            for x in self._root.next_states:
                if x.points == top_score:
                    best_states.append(x)

            return random.choice(best_states)
        else:
            raise GameOver('No one wins.')


class Board:
    WIN = 1
    LOSE = -1
    DRAW = 0

    def __init__(self):
        self.state = []
        for i in range(3):
            buffer = []
            for j in range(3):
                buffer.append(None)
            self.state.extend([buffer])

        self.last_move = (None, None)
        self.last_state = False

        self.free_cells = []
        for i in range(9):
            self.free_cells.append(i + 1)

    def player_move(self, cell):
        """
        Set players point in state by cell as position
        :return: None
        """
        i, j = self.number_cell_to_state_indexes(cell)
        self.state[i][j] = False
        self.free_cells.remove(cell)
        self.last_move = (False, cell)
        if self.analyse_state() == self.LOSE:
            raise GameOver('Player won!')
        elif self.last_state:
            raise GameOver('No one won.')

    def computer_move(self):
        """
        Set computer point in state
        Position determines by points of next possible steps
        :return:
        """
        tree = Tree(self.state, self.last_move)
        next_state = tree.choose_next_move()
        current_move = next_state.last_move
        i, j = self.number_cell_to_state_indexes(current_move[1])
        self.free_cells.remove(current_move[1])
        self.state[i][j] = current_move[0]
        self.last_move = current_move
        if next_state.last_state:
            if next_state.points == self.WIN:
                raise GameOver('Computer won!')
            else:
                raise GameOver('No one won.')

    def analyse_state(self):
        """
        Analysing current state.
        If there is winning combinations or no more steps.
        :return: points of analysing
        """
        cells = [[(i, j) for j in range(3)] for i in range(3)]
        cells += [[(j, i) for j in range(3)] for i in range(3)]
        cells += [[(i, i) for i in range(3)]]
        cells += [[(i, 2 - i) for i in range(3)]]
        for combination in cells:
            value = set()
            for i, j in combination:
                value.add(self.state[i][j])
            if len(value) == 1:
                if True in value:
                    self.last_state = True
                    return self.WIN
                elif False in value:
                    self.last_state = True
                    return self.LOSE
        if not self.free_cells:
            self.last_state = True
        return self.DRAW

    @staticmethod
    def number_cell_to_state_indexes(number):
        """
        :param number: number of cell in board
        :return: cell as indexes in state
        """
        return (number - 1) // 3, (number - 1) % 3

    def __str__(self):
        """
        Return the view of the board.
        """
        result = []
        for i, row in enumerate(self.state):
            row_str = []
            for j, col in enumerate(row):
                row_str.append(str(col) if col is not None else str(i * 3 + j + 1))
            result.append('  ' + '   '.join(row_str) + '  ')
        return '\n{} \n'.format('\n             \n'.join(result))

class Tnode(Board):
    def __init__(self, state, last_move):

        self.state = state
        self.last_move = last_move
        self.free_cells = []

        for i, row in enumerate(state):
            for j, elem in enumerate(row):
                if elem is None:
                    self.free_cells.append(i * 3 + j + 1)
        self.next_states = []
        self.points = 0
        self.last_state = False

    def __gt__(self, other):
        return self.points > other.points

class GameOver(Exception):
    pass
