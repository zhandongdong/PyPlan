from abstract import abssimulator
from copy import deepcopy
from actions import connect4action
from states import connect4state


class Connect4SimulatorClass(abssimulator.AbstractSimulator):
    def __init__(self, num_players, boardwidth = 7, boardheight = 6):
        self.playerturn = 1
        self.current_state = connect4state.Connect4StateClass(num_players)
        self.numplayers = num_players
        self.starting_player = 1
        self.winningplayer = None
        self.gameover = False
        self.board_width = boardwidth
        self.board_height = boardheight

    def reset_simulator(self):
        self.playerturn = self.starting_player
        self.winningplayer = None
        self.current_state = connect4state.Connect4StateClass(self.numplayers)
        self.gameover = False

    def change_simulator_values(self, current_state, player_turn):
        self.playerturn = player_turn
        self.winningplayer = None
        self.set_state(current_state)

    def change_turn(self):
        self.playerturn += 1
        self.playerturn = self.playerturn % self.numplayers

        if self.playerturn == 0:
            self.playerturn = self.numplayers

    def take_action(self, action):
        # CHANGE NEEDED
        actionvalue = action.get_action()
        position = actionvalue['position']
        value = actionvalue['value']

        self.current_state.get_current_state()[value - 1] |= 1 << position
        self.gameover = self.is_terminal()

        reward = [0.0] * self.numplayers
        reward[self.playerturn - 1] -= 1.0

        if self.winningplayer is not None:
            for player in xrange(self.numplayers):
                if player == self.winningplayer - 1:
                    reward[player] += 3.0
                else:
                    reward[player] -= 3.0

        return reward

    def get_valid_actions(self):
        actions_list = []
        current_board = 0

        for player_board in xrange(self.numplayers):
            current_board |= self.current_state.get_current_state()[player_board]

        board_size = ((self.board_height + 1) * self.board_width)
        current_board = bin(current_board)[2:].zfill(board_size)[::-1]
        for column in xrange(self.board_width):
            curr_val = (self.board_height + ((self.board_height + 1) * column))
            curr_val -= 1
            if int(current_board[curr_val]) == 0:
                while curr_val >= (self.board_height + 1) * column:
                    if int(current_board[curr_val]) == 1:
                        actions_list.append(connect4action.Connect4ActionClass(action))
                        break
                    else:
                        action = {}
                        action['position'] = curr_val
                        action['value'] = self.playerturn

                    if (curr_val == self.board_width * column):
                        actions_list.append(connect4action.Connect4ActionClass(action))

                    curr_val -= 1

        return actions_list

    def set_state(self, state):
        self.current_state = deepcopy(state)

    def is_terminal(self):
        for player in xrange(self.numplayers):
            curr_board = self.current_state.get_current_state()[player]
            temp = bin(curr_board)

            #LEFT DIAGONAL
            transform = curr_board & (curr_board >> self.board_height)
            if transform & (transform >> (2 * self.board_height)):
                self.winningplayer = player + 1
                return True

            #RIGHT DIAGONAL
            transform = curr_board & (curr_board >> (self.board_width + 1))
            if transform & (transform >> (2 * (self.board_width + 1))):
                self.winningplayer = player + 1
                return True

            #HORIZONTAL
            transform = curr_board & (curr_board >> self.board_width)
            if transform & (transform >> (2 * self.board_width)):
                self.winningplayer = player + 1
                return True

            #VERTICAL
            transform = curr_board & (curr_board >> 1)
            if transform & (transform >> 2):
                self.winningplayer = player + 1
                return True

        #NO WINS BUT CHECK FOR DRAW
        current_board = 0

        for player_board in xrange(self.numplayers):
            current_board |= self.current_state.get_current_state()[player_board]

        board_size = (self.board_height * self.board_width) + self.board_height
        current_board = bin(current_board)[2:].zfill(board_size)[::-1]
        excluded_vals = [(self.board_height + (self.board_height + 1) * x) for x in xrange(self.board_width)]

        for val in xrange(board_size):
            if val not in excluded_vals:
                if int(current_board[val]) == 0:
                    return False

        return True

    def print_board(self):
        curr_row = self.board_height
        output = ""
        while curr_row >= 0:
            curr_col = 0
            while curr_col < self.board_width:
                board_size = ((self.board_height + 1) * self.board_width)
                player_num = 1
                is_printed = False
                for player_board in self.current_state.get_current_state():
                    curr_board = bin(player_board)[2:].zfill(board_size)[::-1]
                    if int(curr_board[curr_row + ((self.board_height + 1) * curr_col)]) == 1:
                        output += str(player_num) + ""
                        is_printed = True
                    player_num += 1

                if (is_printed == False):
                    output += "0"

                curr_col += 1

            output += "\n"

            curr_row -= 1

        return output