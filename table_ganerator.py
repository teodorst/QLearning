from random import choice, randint
# ma gandesc sa fac un arbore minim de acoperire


from utils import distance, validate_wall_item, validate_item

class TableGenerator(object):

    def __init__(self):
        super(TableGenerator, self).__init__()

    @staticmethod
    def write_table(table, portals, filename):
        rooms_no = len(table)

        with open(filename, 'w') as output_file:
            output_file.write('%d\n' % rooms_no)
            for room in range(rooms_no):
                # Mark new room
                output_file.write('\n')
                room_lines = len(table[room])
                for line in range(room_lines):
                    output_file.write(','.join(table[room][line]) + '\n')

            # Mark portals
            output_file.write('\n')
            for portal in portals:
                # print portal
                output_file.write(' '.join(str(s) for s in portal) + '\n')

    @staticmethod
    def read_table(filename):
        portals = []
        castle = []

        with open(filename, 'r') as input_file:
            rooms_no = 0
            current_room = -1
            first_line = True
            castle_line = False
            portal_line = False
            for line in input_file:
                if first_line:
                    rooms_no = int(line)
                    castle = [[] for _ in range(rooms_no)]
                    first_line = False
                    castle_line = True
                elif castle_line:
                    if not line.strip():
                        current_room += 1
                        if current_room == rooms_no:
                            castle_line = False
                            portal_line = True
                    else:
                        castle[current_room].append(line.split(','))

                elif portal_line:
                    numbers = [x for x in line if x.isdigit()]
                    portals.append(
                        ((numbers[0], numbers[1], numbers[2]),
                         (numbers[3], numbers[4], numbers[5])))

        return portals, table

    @staticmethod
    def validate_points(point1, point2):
        return distance(point1, point2) >= 2

    @staticmethod
    def print_castle(castle, rooms_no, rooms_dimensions):
        for room in range(rooms_no):
            print "Room %d" % room
            for room_line in range(rooms_dimensions[room][0]):
                print castle[room][room_line]

    @staticmethod
    def generate_new_portal(sources, targets, rooms_dimensions):
        room1 = choice(sources)
        room2 = choice(targets)
        while room2 == room1:
            room2 = choice(targets)

        room1_dims = rooms_dimensions[room1]
        room2_dims = rooms_dimensions[room2]
        room1_coords = (randint(0, room1_dims[0] - 1), randint(0, room1_dims[1] - 1))
        room2_coords = (randint(0, room2_dims[0] - 1), randint(0, room2_dims[1] - 1))
        new_portal = ((room1, room1_coords[0], room1_coords[1]),
                      (room2, room2_coords[0], room2_coords[1]))
        return new_portal

    @staticmethod
    def validate_portal(current_portals, new_portal):
        new_room1, new_room2 = new_portal
        ok_flag = True
        for portal in current_portals:
            room1, room2 = portal
            if new_room1[0] == room1[0]:
                if not TableGenerator.validate_points([new_room1[1], new_room1[2]],
                                                      [room1[1], room1[2]]):
                    ok_flag = False
                    break

            if new_room2[0] == room2[0]:
                if not TableGenerator.validate_points([new_room2[1], new_room2[2]],
                                                      [room2[1], room2[2]]):
                    ok_flag = False
                    break

            if new_room1[0] == room2[0]:
                if not TableGenerator.validate_points([new_room1[1], new_room1[2]],
                                                      [room2[1], room2[2]]):
                    ok_flag = False
                    break

            if new_room2[0] == room1[0]:
                if not TableGenerator.validate_points([new_room2[1], new_room2[2]],
                                                      [room1[1], room1[2]]):
                    ok_flag = False
                    break

        return ok_flag

    @staticmethod
    def generate_portals(rooms_no, rooms_dimensions, portals_no, start_room):
        # Ma asigur ca o sa conectez toate camerele
        # Portal este (room, x, y)
        connected_rooms = [start_room]
        disconnected_rooms = [room for room in range(rooms_no) if room != start_room]
        portals_counter = 0
        portals = []
        print disconnected_rooms
        while len(disconnected_rooms):
            new_portal = TableGenerator.generate_new_portal(connected_rooms, disconnected_rooms,
                                                            rooms_dimensions)

            if TableGenerator.validate_portal(portals, new_portal):
                disc_room = new_portal[1][0]
                connected_rooms.append(disc_room)
                disconnected_rooms.remove(disc_room)
                portals_counter += 1
                portals.append(new_portal)


        while portals_counter < portals_no:
            new_portal = TableGenerator.generate_new_portal(connected_rooms, connected_rooms,
                                                            rooms_dimensions)
            if TableGenerator.validate_portal(portals, new_portal):
                portals_counter += 1
                portals.append(new_portal)

        return portals

    @staticmethod
    def generate_treasures(treasures_no, rooms_no, rooms_dimensions, castle):
        treasures_contor = 0
        treasures = []
        while treasures_contor < treasures_no:
            treasure_room = randint(0, rooms_no - 1)
            treasure_x = randint(0, rooms_dimensions[treasure_room][0] - 1)
            treasure_y = randint(0, rooms_dimensions[treasure_room][1] - 1)
            treasure = (treasure_room, treasure_x, treasure_y)
            if validate_item(castle[treasure_room], (treasure_x, treasure_y)):
                treasures.append(treasure)
                treasures_contor += 1
                castle[treasure_room][treasure_x][treasure_y] = 'T'
        return treasures


    @staticmethod
    def generate_walls(walls_no, rooms_no, rooms_dimensions, castle):
        walls = []
        walls_contor = 0
        while walls_contor < walls_no:
            wall_room = randint(0, rooms_no - 1)
            wall_x = randint(0, rooms_dimensions[wall_room][0] - 1)
            wall_y = randint(0, rooms_dimensions[wall_room][1] - 1)
            wall = (wall_room, wall_x, wall_y)
            if validate_wall_item(castle[wall_room], (wall_x, wall_y)):
                walls.append(wall)
                walls_contor += 1
                castle[wall_room][wall_x][wall_y] = '#'

        return walls

    @staticmethod
    def generate_guardians(guardians_no, rooms_no, rooms_dimensions, castle):
        guardians = []
        guardians_contor = 0
        rooms_filled = set()

        while guardians_contor < guardians_no:
            guardian_room = randint(0, guardians_no - 1)
            guardian_x = randint(0, rooms_dimensions[guardian_room][0] - 1)
            guardian_y = randint(0, rooms_dimensions[guardian_room][1] - 1)
            if (validate_item(castle[guardian_room], (guardian_x, guardian_y)) and
                    guardian_room not in rooms_filled):
                guardians.append((guardian_room, guardian_x, guardian_y))
                guardians_contor += 1
                castle[guardian_room][guardian_x][guardian_y] = 'G'
                rooms_filled.add(guardian_room)
        return guardians

    @staticmethod
    def generate_start_and_end(rooms_no, rooms_dimensions, castle):
        rooms = range(rooms_no)
        start_room = choice(rooms)
        rooms.remove(start_room)
        end_room = choice(rooms)

        start_x = randint(0, rooms_dimensions[start_room][0] - 1)
        start_y = randint(0, rooms_dimensions[start_room][1] - 1)
        while not validate_item(castle[start_room], (start_x, start_y)):
            start_x = randint(0, rooms_dimensions[start_room][0] - 1)
            start_y = randint(0, rooms_dimensions[start_room][1] - 1)

        end_x = randint(0, rooms_dimensions[end_room][0] - 1)
        end_y = randint(0, rooms_dimensions[end_room][1] - 1)
        while not validate_item(castle[end_room], (end_x, end_y)):
            end_x = randint(0, rooms_dimensions[end_room][0] - 1)
            end_y = randint(0, rooms_dimensions[end_room][1] - 1)

        castle[start_room][start_x][start_y] = 'H'
        castle[end_room][end_x][end_y] = 'F'
        return ((start_room, start_x, start_y), (end_room, end_x, end_y))

    @staticmethod
    def generate_table(rooms_no, rooms_dimensions, guardians_no, portals_no,
                       treasures_no, walls_no):
        if guardians_no > rooms_no:
            return None

        castle = [[['_' for _ in range(rooms_dimensions[i][1])] for _ in
                   range(rooms_dimensions[i][0])] for i in range(rooms_no)]


        print "Generating portals ..."
        portals = TableGenerator.generate_portals(rooms_no, rooms_dimensions, portals_no, 0)
        for portal in portals:
            entry, out = portal
            castle[entry[0]][entry[1]][entry[2]] = 'P'
            castle[out[0]][out[1]][out[2]] = 'P'

        print "Generating treasures ..."
        TableGenerator.generate_treasures(treasures_no, rooms_no, rooms_dimensions, castle)

        print "Generating walls ..."
        TableGenerator.generate_walls(walls_no, rooms_no, rooms_dimensions, castle)

        print "Generating garidans ..."
        TableGenerator.generate_guardians(guardians_no, rooms_no, rooms_dimensions, castle)

        TableGenerator.generate_start_and_end(rooms_no, rooms_dimensions, castle)

        TableGenerator.print_castle(castle, rooms_no, rooms_dimensions)

        return portals, castle


if __name__ == '__main__':
    table_generator = TableGenerator()
    portals, table = table_generator.generate_table(5, [(10, 10), (10, 10), (10, 10), (10, 10),
                                                        (10, 10)], 5, 10, 10, 40)
    table_generator.write_table(table, portals, 'test.txt')

    portals2, table2 = table_generator.read_table('test.txt')
    # print table2
    print portals2

