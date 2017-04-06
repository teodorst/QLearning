from table_ganerator import TableGenerator
from copy import deepcopy
from utils import distance
from random import choice
from time import sleep


TREASURE_REWARD = 100
FINISH_REWARD = 1000
STEP_REWARD = -1

GUARD_INVALID_CODES = ['#', 'P', 'T']
HERO_INVALID_CODES = ['#', 'P', 'T']

class Game(object):
    def __init__(self, filename, radius):
        super(Game, self).__init__()
        self.current_pos = None
        self.configure_game(filename)
        self.radius = radius
        self.reset_game()

    def configure_game(self, filename):
        table_gen = TableGenerator()
        portals, game_map = table_gen.read_table(filename)
        self.game_map = game_map
        self.initial_rewards = {}
        self.initial_guards = list()
        self.rooms_no = len(game_map)
        self.rooms_dim = [(len(game_map[x]), len(game_map[x][0])) for x in range(self.rooms_no)]
        self.portals = []
        self.start_pos = None
        self.finish_pos = None
        self.curr_game_rewards = deepcopy(self.game_map)
        for portal in portals:
            entry, out = portal
            self.portals.append((entry, out))
            self.portals.append((out, entry))

        for room in range(self.rooms_no):
            room_reward = 0
            for i in range(self.rooms_dim[room][0]):
                for j in range(self.rooms_dim[room][1]):
                    if self.game_map[room][i][j] == 'T':
                        self.initial_rewards[(room, i, j)] = TREASURE_REWARD
                        room_reward += TREASURE_REWARD
                        self.curr_game_rewards[room][i][j] = TREASURE_REWARD
                    elif self.game_map[room][i][j] == 'F':
                        self.initial_rewards[(room, i, j)] = FINISH_REWARD
                        self.finish_pos = (room, i, j)
                        room_reward += FINISH_REWARD
                        self.curr_game_rewards[room][i][j] = FINISH_REWARD
                    elif self.game_map[room][i][j] == 'G':
                        self.initial_guards.append((room, i, j))
                        self.curr_game_rewards[room][i][j] = STEP_REWARD
                    elif self.game_map[room][i][j] == 'H':
                        self.start_pos = (room, i, j)
                        self.last_hero_step = '_'
                        self.curr_game_rewards[room][i][j] = STEP_REWARD
                    else:
                        self.curr_game_rewards[room][i][j] = STEP_REWARD

                for portal in self.portals:
                    entry, out = portal
                    print entry, out
                    if out[0] == room:
                        self.initial_rewards[entry] = room_reward



    def reset_game(self):
        self.curr_game_map = deepcopy(self.game_map)
        self.rewards = deepcopy(self.initial_rewards)
        self.guards = deepcopy(self.initial_guards)
        self.current_pos = deepcopy(self.start_pos)
        self.is_finished = False
        self.score = 0

    def print_game_initial_configuration(self):

        for room in range(self.rooms_no):
            print 'Room %d' % room
            dim_x, _ = self.rooms_dim[room]
            for i in range(dim_x):
                print self.game_map[room][i]

        print 'Start pos: ', self.start_pos
        print 'Finish pos: ', self.start_pos
        print 'Guards '
        for guard in self.initial_guards:
            print guard

        print 'Rewards: '
        for pos in self.initial_rewards:
            print pos, self.initial_rewards[pos]

    def print_current_game(self):
        for room in range(self.rooms_no):
            if room == self.current_pos[0]:
                dim_x, _ = self.rooms_dim[room]
                for i in range(dim_x):
                    print self.curr_game_map[room][i]
        # This is for DEBUG
        # print 'Guards '
        # for guard in self.guards:
        #     print guard

        # print 'Rewards: '
        # for pos in self.rewards:
        #     print pos, self.rewards[pos]


    def next_guard_pos(self, g_row, g_col):
        h_room, h_row, h_col = self.current_pos
        dy, dx = h_row - g_row, h_col - g_col

        is_good = lambda dr, dc: self._valid_pos(h_room, g_row + dr, g_col + dc,
                                                 GUARD_INVALID_CODES)

        next_g_row, next_g_col = g_row, g_col
        if abs(dy) > abs(dx) and is_good(int(dy / abs(dy)), 0):
            next_g_row = g_row + int(dy / abs(dy))
        elif abs(dx) > abs(dy) and is_good(0, int(dx / abs(dx))):
            next_g_col = g_col + int(dx / abs(dx))
        else:
            options = []
            if abs(dx) > 0:
                if is_good(0, int(dx / abs(dx))):
                    options.append((g_row, g_col + int(dx / abs(dx))))
            else:
                if is_good(0, -1):
                    options.append((g_row, g_col - 1))
                if is_good(0, 1):
                    options.append((g_row, g_col + 1))
            if abs(dy) > 0:
                if is_good(int(dy / abs(dy)), 0):
                    options.append((g_row + int(dy / abs(dy)), g_col))
            else:
                if is_good(-1, 0):
                    options.append((g_row - 1, g_col))
                if is_good(1, 0):
                    options.append((g_row + 1, g_col))

            if len(options) > 0:
                next_g_row, next_g_col = choice(options)
        return next_g_row, next_g_col

    def move_guard(self, g_pos):
        g_x, g_y = g_pos
        room = self.current_pos[0]
        # Move guard
        self.curr_game_map[room][g_x][g_y] = '_'
        g_x, g_y = self.next_guard_pos(g_x, g_y)
        self.curr_game_map[room][g_x][g_y] = 'G'
        return g_x, g_y


    def _valid_gurd_pos(self, room, pos_x, pos_y):
        return self._valid_pos(room, pos_x, pos_y, GUARD_INVALID_CODES)

    def _valid_hero_pos(self, room, pos_x, pos_y):
        return self._valid_pos(room, pos_x, pos_y, HERO_INVALID_CODES)

    def _valid_pos(self, room, pos_x, pos_y, invalid_codes):
        room_x, room_y = self.rooms_dim[room]
        return (pos_x >= 0 and pos_x < room_x and pos_y >= 0 and pos_y < room_y and
                self.curr_game_map[room][pos_x][pos_y] not in invalid_codes)

    def game_move(self, action):
        new_state, reward = self.apply_action(action)
        g_pos, _ = self.deserialize_state(state)
        # Here i will apply move
        if g_pos:
            g_pos = self.move_guard(g_pos)


        new_state_serialized = self.serialize_state()
        return new_state_serialized, reward

    def apply_action(self, action):
        h_r, h_x, h_y = self.current_pos
        next_h_r, next_h_x, next_h_y = self.current_pos

        if action == 'RIGHT':
            next_h_x, next_h_y = h_x, h_y + 1
        elif action == 'LEFT':
            next_h_x, next_h_y = h_x, h_y - 1
        elif action == 'UP':
            next_h_x, next_h_y = h_x - 1, h_y
        elif action == 'DOWN':
            next_h_x, next_h_y = h_x + 1, h_y
        else:
            next_h_x, next_h_y = h_x, h_y

        new_reward = 0
        # Portal case
        if self.curr_game_map[next_h_r][next_h_x][next_h_y] == 'P':
            portal = [x for x in self.portals if x[0] == (next_h_r, next_h_x, next_h_y)][0]
            next_h_r, next_h_x, next_h_y = portal[1]
            # update ex reward here

        new_reward = self.curr_game_rewards[next_h_r][next_h_x][next_h_y]
        #update pos
        print self.current_pos, (next_h_r, next_h_x, next_h_y)
        self.current_pos = (next_h_r, next_h_x, next_h_y)
        if self.last_hero_step != 'T':
            self.curr_game_map[h_r][h_x][h_y] = self.last_hero_step

        self.last_hero_step = self.curr_game_map[next_h_r][next_h_x][next_h_y]
        self.curr_game_map[next_h_r][next_h_x][next_h_y] = 'H'

        new_state = self.serialize_state()
        return new_state, new_reward

    def is_final_state(self):
        return self.current_pos == self.finish_pos

    def serialize_state(self):
        h_r, h_x, h_y = self.current_pos
        r_x, r_y = self.rooms_dim[h_r]
        space_right = self.radius if h_y + self.radius < r_y else r_y - h_y - 1
        space_left = self.radius if h_y - self.radius >= 0 else h_y
        space_up = self.radius if h_x - self.radius >= 0 else h_x
        space_down = self.radius if h_x + self.radius < r_x else r_x - h_x - 1
        state_col_no = space_left + space_right + 1
        state_row_no = space_up + space_down + 1
        s_x, s_y = h_x - space_up, h_y - space_left
        new_state = []
        for i in range(state_row_no):
            for j in range(state_col_no):
                new_state.append(self.curr_game_map[h_r][s_x + i][s_y + j])
        serialized_state = ''.join(new_state)
        return serialized_state

    def deserialize_state(self, state):
        g_pos = None
        h_r, _, h_y = self.current_pos
        _, r_y = self.rooms_dim[h_r]
        space_right = self.radius if h_y + self.radius < r_y else r_y - h_y - 1
        space_left = self.radius if h_y - self.radius >= 0 else h_y
        state_col_no = space_left + space_right + 1

        g_location = 0
        for i in state:
            if i == 'G':
                g_pos = g_location / state_col_no, g_location % state_col_no
                break
            g_location += 1

        state_extended = []

        for i in range(0, len(state), state_col_no):
            state_extended.append(list(state[i:i+state_col_no]))

        return g_pos, state_extended


    # def print_game_state(self, state):


if __name__ == '__main__':
    game = Game('test.txt', 2)
    game.print_game_initial_configuration()
    # game.print_current_game()
    for _ in range(10):
        state = game.serialize_state()
        _, state1 = game.deserialize_state(state)
        for h in state1:
            print h
        print ''
        sleep(0.5)
        state, reward = game.game_move('RIGHT')
        _, state = game.deserialize_state(state)
        for h in state:
            print h
        print ''
        sleep(0.5)


