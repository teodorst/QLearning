from table_ganerator import TableGenerator

TREASURE_REWARD = 100
FINISH_REWARD = 500

class Game(object):
    def __init__(self, filename):
        super(Game, self).__init__()
        self.configure_game(filename)

    def configure_game(self, filename):
        table_gen = TableGenerator()
        portals, game_map = table_gen.read_table(filename)
        self.game_map = game_map
        self.initial_rewards = {}
        self.initial_guards = set()
        self.rooms_no = len(game_map)
        self.rooms_dim = [(len(game_map[i]), len(game_map[i][0])) for i in range(self.rooms_no)]
        self.portals = []
        self.start_pos = None
        self.finish_pos = None
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
                    elif self.game_map[room][i][j] == 'F':
                        self.initial_rewards[(room, i, j)] = FINISH_REWARD
                        self.finish_pos = (room, i, j)
                        room_reward += FINISH_REWARD
                    elif self.game_map[room][i][j] == 'G':
                        self.initial_guards.add((room, i, j))
                    elif self.game_map[room][i][j] == 'H':
                        self.start_pos = (room, i, j)

                for portal in self.portals:
                    entry, out = portal
                    print entry, out
                    if out[0] == room:
                        self.initial_rewards[entry] = room_reward

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


if __name__ == '__main__':
    game = Game('test.txt')
    game.print_game_initial_configuration()




# ## Move to next state
# def apply_action(str_state, action):
#     assert(action in ACTIONS)
#     message = "Greuceanu moved %s." % action

#     state = __deserialize_state(str_state)
#     g_row, g_col = __get_position(state, "G")
#     assert(g_row >= 0 and g_col >= 0)             # Greuceanu must be on the map

#     next_g_row = g_row + ACTION_EFFECTS[action][0]
#     next_g_col = g_col + ACTION_EFFECTS[action][1]

#     if not __is_valid_cell(state, next_g_row, next_g_col):
#         next_g_row = g_row
#         next_g_col = g_col
#         message = message + " Not a valid cell there."

#     state[g_row][g_col] = " "
#     if state[next_g_row][next_g_col] == "B":
#         message = message + " Greuceanu stepped on the balaur."
#         return __serialize_state(state), LOSE_REWARD, message
#     elif state[next_g_row][next_g_col] == "o":
#         state[next_g_row][next_g_col] = "G"
#         message = message + " Greuceanu found 'marul fermecat'."
#         return __serialize_state(state), WIN_REWARD, message
#     state[next_g_row][next_g_col] = "G"

#     ## Balaur moves now
#     b_row, b_col = __get_position(state, "B")
#     assert(b_row >= 0 and b_col >= 0)

#     dy, dx = next_g_row - b_row, next_g_col - b_col

#     is_good = lambda dr, dc:__is_valid_cell(state, b_row + dr, b_col + dc)

#     next_b_row, next_b_col = b_row, b_col
#     if abs(dy) > abs(dx) and is_good(int(dy / abs(dy)), 0):
#         next_b_row = b_row + int(dy / abs(dy))
#     elif abs(dx) > abs(dy) and is_good(0, int(dx / abs(dx))):
#         next_b_col = b_col + int(dx / abs(dx))
#     else:
#         options = []
#         if abs(dx) > 0:
#             if is_good(0, int(dx / abs(dx))):
#                 options.append((b_row, b_col + int(dx / abs(dx))))
#         else:
#             if is_good(0, -1):
#                 options.append((b_row, b_col - 1))
#             if is_good(0, 1):
#                 options.append((b_row, b_col + 1))
#         if abs(dy) > 0:
#             if is_good(int(dy / abs(dy)), 0):
#                 options.append((b_row + int(dy / abs(dy)), b_col))
#         else:
#             if is_good(-1, 0):
#                 options.append((b_row - 1, b_col))
#             if is_good(1, 0):
#                 options.append((b_row + 1, b_col))

#         if len(options) > 0:
#             next_b_row, next_b_col = choice(options)

#     if state[next_b_row][next_b_col] == "G":
#         message = message + " The balaur ate Greuceanu."
#         reward = LOSE_REWARD
#     elif state[next_b_row][next_b_col] == "o":
#         message = message + " The balaur found marul fermecat. Greuceanu lost!"
#         reward = LOSE_REWARD
#     else:
#         message = message + " The balaur follows Greuceanu."
#         reward = MOVE_REWARD

#     state[b_row][b_col] = " "
#     state[next_b_row][next_b_col] = "B"

#     return __serialize_state(state), reward, message

