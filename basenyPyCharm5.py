# baseny
# unicode icons: http://xahlee.info/comp/unicode_geometric_shapes.html
import time, examples


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [str(a) + '.' + str(b) for a in A for b in B]


#### PARAMS
riddle = examples.riddle_a04473

no = '.'  # no info
ho = '\u23cf'  # house '\u2395'
em = '-'  # empty
at = '(\u02c4)'  # arrow top [2]
ar = '(\u02c3)'  # arrow right [3]
ad = "(\u02c5)"  # arrow down [0]
al = '(\u02c2)'  # arrow left [1]
na = 'o'  # tank without arrow
col_header = riddle.split(";")[0].split(",")
row_header = riddle.split(";")[1].split(",")
grid = riddle.split(";")[2]
rows = list(a for a in range(1, len(row_header) + 1))
rowsr = list('r' for a in range(1, len(row_header) + 1))  # rrrrrr...
row_no = list(a for a in range(1, len(row_header) + 1))  # 1,2,3,4....
cols = list(a for a in range(1, len(col_header) + 1))
colsc = list('c' for a in range(1, len(col_header) + 1))  # cccccc....
col_no = list(a for a in range(1, len(col_header) + 1))  # 1,2,3,4....
rows_str = list(str(a) for a in rows)
squares = cross(rows, cols)
dict_nghb_tank = {'2': at, '3': ar, '0': ad, '1': al}
dict_nghb_rev = {0: '2', 1: '3', 2: '0', 3: '1'}  # reversed dict of neighbours

# generation of unitlist,
# should be reduced to 1 line, but cross() is splitting 10 into 1 and 0
# unitlist = ([cross(rows, c) for c in cols] +[cross(r, cols) for r in rows])
unit1 = []
unit2 = []
for row in rows:
    for col in cols:
        unit = str(row) + '.' + str(col)
        unit1.append(unit)
    unit2.append(unit1)
    unit1 = []
unitr_zip = list(map(list, zip(rows, row_header, unit2, rowsr,
                               rowsr)))  # second rowsr ascts as a flag if the unit is completed (then x)
unit1 = []
unit2 = []
for col in cols:
    for row in rows:
        unit = str(row) + '.' + str(col)
        unit1.append(unit)
    unit2.append(unit1)
    unit1 = []
unitc_zip = list(map(list, zip(cols, col_header, unit2, colsc, colsc)))
unitlist = unitr_zip + unitc_zip


def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in 'X' or c in '0.']
    grid_dict = dict(zip(squares, chars))
    HOUSES = []
    for square in zip(squares, chars):
        if square[1] == 'X':
            HOUSES.append(square[0])
    for square in grid_dict:
        if grid_dict[square] == no:
            grid_dict[square] = '-0123'
    HOUSES = tuple(HOUSES)
    return grid_dict, HOUSES


def total_length(values):
    total_len = 0
    for square in values:
        total_len += len(values[square])
    return total_len


def display(values, ifall, central):  # Display as 2-D grid
    values_copy = values.copy()
    if ifall == "short":
        for s in values_copy:
            if len(values_copy[s]) > 1 and em not in values_copy[s]:
                values_copy[s] = na
            if len(values_copy[s]) > 1 and em in values_copy[s]:
                values_copy[s] = no
            if values_copy[s] in dict_nghb_tank:  # assign arrows to tank
                values_copy[s] = dict_nghb_tank[values_copy[s]]
    diff_col_header = []
    diff_row_header = []
    for unit in unitc_zip:
        diff_col_header.append(difference_headers_tanks(unit, values)[0])
    for unit in unitr_zip:
        diff_row_header.append(difference_headers_tanks(unit, values)[0])
    "Display these values as a 2-D grid."
    print(' '.center(central) * 2 + 'diff'.center(central) + ' ' +
          ' '.join(str(diff_col_header[c - 1]).center(central) for c in cols))
    print(' '.center(central) * 3 + ' ' + ' '.join(
        ('[' + str(col_no[c - 1]) + ']').center(central) for c in col_no))
    print(' '.center(central) * 2 + 'head'.center(central) + ' ' +
          ' '.join(col_header[c - 1].center(central) for c in cols))
    for r in rows:
        print(str(diff_row_header[r - 1]).center(central) + '[' +
              (str(row_no[r - 1]) + ']').center(central) + row_header[r - 1].center(central) +
              ' '.join(values_copy[str(r) + '.' + str(c)].center(central) for c in cols))
    print()


def run_assertions(values):
    chars = [c for c in grid if c in 'X' or c in '0.']
    all_tanks_list, empties_list, noinfo_list, tanks_assigned, tanks_not_assigned, houses_list = count_symbol(values,
                                                                                                              values)
    assert len(chars) == len(row_header) * len(col_header)
    assert len(HOUSES) == grid.count('X')
    # TODO add assertions
    assert len(all_tanks_list) + len(HOUSES) + len(empties_list) + len(noinfo_list) == len(squares)
    for house in HOUSES:
        empty_house = control_tanks_around_house(values, house)[0] + control_tanks_around_house(values, house)[2]
        if empty_house == 0:
            print('house with no tank slots', house)
        assert control_tanks_around_house(values, house)[0] + control_tanks_around_house(values, house)[2] > 0
        assert control_tanks_around_house(values, house)[2] < 2


def find_neighbours(values, collection, cac, rh):
    a0, empties_list, a2, a3, a4, a5 = count_symbol(values, collection)
    # cac = (Cross, All, Corners), rh - remove houses
    neighbours_dict = {}
    neighbours_set = set()
    for square in collection:
        x = int(square.split('.')[0])
        y = int(square.split('.')[1])
        # define potential neighbour for each square
        if cac == 'All':
            neighbours_local = cross((x - 1, x, x + 1), (y - 1, y, y + 1))
            neighbours_local.remove(square)
        if cac == 'Wide':
            neighbours_local = cross((x - 3, x - 2, x - 1, x, x + 1, x + 2, x + 3),
                                     (y - 3, y - 2, y - 1, y, y + 1, y + 2, y + 3))
            neighbours_local.remove(square)
        elif cac == 'Cross':
            neighbours_local = [(str(x - 1) + '.' + str(y)), (str(x) + '.' + str(y + 1)),
                                (str(x + 1) + '.' + str(y)), (str(x) + '.' + str(y - 1))]
        elif cac == 'Corners':
            neighbours_local = [(str(x - 1) + '.' + str(y - 1)), (str(x - 1) + '.' + str(y + 1)),
                                (str(x + 1) + '.' + str(y - 1)), (str(x + 1) + '.' + str(y + 1))]
        # remove all values outside of the riddle grid
        neighbours_to_remove = []
        for nbour in neighbours_local:
            x1 = int(nbour.split('.')[0])
            y1 = int(nbour.split('.')[1])
            if x1 < 1 or y1 < 1 or x1 > len(row_header) or y1 > len(col_header):
                neighbours_to_remove.append(nbour)
        for neigbour in neighbours_to_remove:
            neighbours_local.remove(neigbour)
        # remove houses and empties
        if rh == 'yes':
            for house in HOUSES:
                if house in neighbours_local:
                    neighbours_local.remove(house)
        for empty in empties_list:
            if empty in neighbours_local:
                neighbours_local.remove(empty)
        # generate output
        neighbours_dict[square] = neighbours_local
        neighbours_set.update(neighbours_local)  # TODO remove it
        for square in collection:
            if square in neighbours_set:
                neighbours_set.remove(square)
    return neighbours_dict, neighbours_set, neighbours_local
    # neighbours_local can be used if collection is single house as list: [house]


def find_neighbours_for_one_house(values, house, reh):
    # TODO use this more often instead of find_neighbours_for_houses which returns list of dictionaries
    # reh - remove houses and empties
    x = int(house.split('.')[0])
    y = int(house.split('.')[1])
    # define potential neighbour for the house
    neighbours_local = [(str(x - 1) + '.' + str(y)), (str(x) + '.' + str(y + 1)),
                        (str(x + 1) + '.' + str(y)), (str(x) + '.' + str(y - 1))]
    # remove all values outside of the boundaries of the grid
    neighbours_to_remove = []
    for nbour in neighbours_local:
        x1 = int(nbour.split('.')[0])
        y1 = int(nbour.split('.')[1])
        if x1 == 0 or y1 == 0 or x1 == len(row_header) + 1 or y1 == len(col_header) + 1:
            neighbours_to_remove.append(nbour)
    for position in neighbours_local:
        for neigbour in neighbours_to_remove:  # remove all values outside of the riddle grid
            if neigbour == position:
                neighbours_local[neighbours_local.index(position)] = ''
    # cleaning values for other neighbours
    if reh == 'yes':
        for position in neighbours_local:
            if position:
                if values[position] == em:
                    neighbours_local[neighbours_local.index(position)] = ''
                if values[position] == 'X':
                    neighbours_local[neighbours_local.index(position)] = ''
                    # print('neighbours_local',neighbours_local)
    return neighbours_local


def find_nghbr_units(square):
    nghbr_units = []
    x = int(square.split('.')[0])
    y = int(square.split('.')[1])
    if y < len(col_header):
        nghbr_units.append(unitc_zip[y])
    if (y - 2) >= 0:
        nghbr_units.append(unitc_zip[y - 2])
    if x < len(row_header):
        nghbr_units.append(unitr_zip[x])
    if (x - 2) >= 0:
        nghbr_units.append(unitr_zip[x - 2])
    return nghbr_units


def count_symbol(values, collection):
    all_tanks_list = []  # len>1 and in '0123'
    tanks_not_assigned = []  # len>1
    tanks_assigned = []  # in '0123'
    empties_list = []  # em
    noinfo_list = []  # '.'
    houses_list = []  # 'X'
    for square in collection:
        if (len(values[square]) > 1 and em not in values[square]) or values[square] in ('0123'):
            all_tanks_list.append(square)
        if len(values[square]) > 1 and em not in values[square]:  # 34 / 0123
            tanks_not_assigned.append(square)
        if values[square] in "0123" and len(values[square]) == 1:
            tanks_assigned.append(square)  # 3 / 4 / 5
        if values[square] == em:
            empties_list.append(square)
        if len(values[square]) > 1 and em in values[square]:
            noinfo_list.append(square)
        if values[square] == 'X':
            houses_list.append(square)
    return all_tanks_list, empties_list, noinfo_list, tanks_assigned, tanks_not_assigned, houses_list
    # all_tanks_list, empties_list, noinfo_list, tanks_assigned, tanks_not_assigned, houses_list=count_symbol(values, collection)


def count_solved_houses(values, collection):  # couldnt use count_symbol due to recursion
    houses_solved = []  # 'X' with one arrow
    houses_not_solved = []  # 'X' with many arrows
    for square in collection:
        if values[square] == 'X':
            count_pot_t, pot_t_list, count_ass_t, ass_t_list = control_tanks_around_house(values, square)
            if count_pot_t == 0 and count_ass_t == 1:
                houses_solved.append(square)
            if count_pot_t > 0:
                houses_not_solved.append(square)
    return houses_solved, houses_not_solved


def stats(values):
    run_assertions(values)
    total_len = total_length(values)
    display(values, '', central)
    display(values, 'short', central)
    all_tanks_list, empties_list, noinfo_list, tanks_assigned, tanks_not_assigned, houses_list = count_symbol(values,
                                                                                                              values)
    print("Total Length:           ", len(grid), '(+' + str(total_len - len(grid)) + ')')
    print("No of HOUSES (solved):  ", len(HOUSES), '(' + str(len(count_solved_houses(values, values)[0])) + ')')
    print("No of tanks (missing):  ", len(all_tanks_list), '(' + str(len(HOUSES) - len(all_tanks_list)) + ')')
    print("No of tanks assigned/na:", str(len(tanks_assigned)) + '/' + str(len(tanks_not_assigned)))
    print("Empty squares (missing):", len(empties_list), '(' +
          str(len(row_header) * len(col_header) - len(HOUSES) * 2 - len(empties_list)) + ')')
    one_n_list = []
    two_n_list = []
    for house in HOUSES:
        count_pot_t, pot_t_list, count_ass_t, ass_t_list = control_tanks_around_house(values, house)
        if count_pot_t == 1:
            one_n_list.append(house)
        if count_ass_t == 1:
            two_n_list.append(house)
    print("Houses with only 1 neighbour available for a tank: ", len(one_n_list), one_n_list)
    print("Houses with 1 assigned tank:       ", len(two_n_list))
    print()
    print()
    print((find_neighbours(values, ['9.18'], 'Cross', 'yes'))[2])
    print(find_neighbours_for_one_house(values, '9.18', 'yes'))
    # TODO completed units r/c


def check_if_solved(values, print_flag):
    run_assertions(values)
    if len(grid) == total_length(values):
        if print_flag == 'print':
            print("SOLVED! Yippee Ki Yay!!!")
        return True
    else:
        if print_flag == 'print':
            print("Not yet solved. Try harder!")
        return False


def assign_tank(values, square, house, arrow, print_flag):
    candidates = find_neighbours(values, [square], 'All', 'yes')[0][square]
    # arrow points to a house - is this house free?
    assd_t_for_pote_house = 0
    if arrow == '0123':
        arrow = values[square].replace('-', '')
    if len(arrow) == 1 and len(house) > 0:  # if arrow is 0123, I skip this check
        assd_t_for_pote_house = control_tanks_around_house(values, house)[2]
    # tank assignment
    if len(values[square]) > 1 and assd_t_for_pote_house == 0:  # removed: em in values[square] and
        if print_flag == 'print':
            print()
            print('For square:', square, 'of value: ', values[square])
            print('possible squares to be assigned (-):', candidates)
        values[square] = arrow
        for candidate in candidates:  ##0
            if len(values[candidate]) > 1 and em in values[candidate]:
                if print_flag == 'print':
                    print('##0 ', candidate, ' Changed ', values[candidate], ' to ', em)
                values[candidate] = em
    else:
        if print_flag == 'print':
            print("Wrong square!")
    return values


def count_sections_in_units(unit, values):
    # print(unit[3], unit[0], ' |unit header: ', unit[1], ' |Tanks: ', tanks, ' |Difference: ', int(tanks) - (int(unit[1]) - int(tanks)))
    unit_content = ''  # example: 011011000101001
    for z in unit[2]:
        if len(values[z]) > 1 and em in values[z]:
            unit_content += '1'
        else:
            unit_content += '0'

    # creates holes list
    holes_listing = []  # example: [['1.19', '2.19', '3.19'], ['5.19'], ['7.19', '8.19', '9.19', '10.19', '11.19'], ['13.19'], ['15.19']]
    number_of_holes = 0  # example above has 8 holes in it
    holes_list = []  # example: [3, 1, 5, 1, 1]

    for i in range(len(unit_content)):
        letter = unit_content[i]  # letter is probably 'hole slot'
        if letter == '1' and (unit_content[i - 1] == '0' or i == 0):  # the slot starts
            false_flag = 'False'
            slot = [unit[2][i]]  # the slot starts
            while false_flag == 'False' and i < len(unit_content) - 1:
                if unit_content[i + 1] == '1':  # check the next square and enlarge the slot
                    letter += unit_content[i + 1]
                    slot.append(unit[2][i + 1])
                    i += 1
                else:
                    false_flag = 'True'
            holes_list.append(len(letter))
            holes_listing.append(slot)

    # checks number of slots in each hole
    for hole in holes_list:
        hole_slot = 0
        if int(hole) == 1:
            hole_slot = 1
            # print('1','hole',hole,'hole_slot',hole_slot)
        elif int(hole) % 2 == 0:
            hole_slot = int(hole) / 2
            # print('2','hole', hole, 'hole_slot', hole_slot)
        else:
            hole_slot = (int(hole) + 1) / 2
            # print('3','hole', hole, 'hole_slot', hole_slot)
        number_of_holes += hole_slot
    tanks_list = count_symbol(values, unit[2])[0]
    difference = number_of_holes - (int(unit[1]) - len(tanks_list))
    if difference < 0:
        print()
        print('unit:', unit[3], unit[0], '|diff:', difference, '|num of holes:', number_of_holes,
              '|header:', int(unit[1]), '|count tanks:', len(tanks_list))
    return difference, holes_list, holes_listing
    # TODO address scenario where diff=1 and there is -.-.-, then add - above and below


def difference_headers_tanks(unit, values):
    # eliminate_arrows(values)
    values_test = values.copy()
    unit_new_values = []
    # arrow_order: algorithm moves right and down, assign tanks from left and top
    if unit[3] == 'r':
        arrow_order = '3201'
    elif unit[3] == 'c':
        arrow_order = '0132'
    for square in unit[2]:
        all_tanks_list, empties_list, noinfo_list, tanks_assigned, tanks_not_assigned, houses_list = count_symbol(
            values_test, unit[2])
        if square in noinfo_list:
            arrow = values_test[square].replace(em, '')  # by removing '-' I change it into tank
            i = 0
            while len(arrow) > 1:  # remove arrows until there is only one
                arrow = arrow.replace(arrow_order[i], '')
                i += 1
            values_test = assign_tank(values_test, square, '', arrow, '')
        elif square in houses_list:
            house_with_arrow_clean_nghb(values_test, square, '')
        unit_new_values += values_test[square]
    all_tanks_list = count_symbol(values_test, unit[2])[0]
    difference = len(all_tanks_list) - int(unit[1])
    return difference, unit_new_values


def difference_headers_tanks_solve(values):
    for unit in unitlist:
        difference, unit_new_values = difference_headers_tanks(unit, values)
        print("\nnew unit values:", unit_new_values)
        print(unit[3], unit[0], 'difference:', difference)
        # if difference == 1:
        #    print(unit[3], unit[0], 'difference:', difference)
        # elif difference <0:
        #    print('WARNING! Diff<0 | Not enough placeholders for tanks in unit:',unit[3]+unit[0])
        # elif difference==0:
        # TODO finish this and remove clean_unit_sections_diff_zero
        # all adjasent units - change no info into '-'
        # all single slots transform into tank


def control_tanks_around_house(values, house):  # pass only one tank ID as a [list] (like [3.20])
    neighbours_list = find_neighbours_for_one_house(values, house, 'yes')
    count_potential_tanks = 0
    potential_tanks_list = ['', '', '', '']
    count_assigned_tanks = 0
    assigned_tanks_list = ['', '', '', '']
    for i in range(0, 4):
        if neighbours_list[i]:  # neighbour will be empty '' if the value for it was '-'
            if str(i) in values[neighbours_list[i]] and len(values[neighbours_list[i]]) > 1:
                count_potential_tanks += 1
                potential_tanks_list[i] = neighbours_list[i]
            if str(i) in values[neighbours_list[i]] and len(values[neighbours_list[i]]) == 1:
                count_assigned_tanks += 1
                assigned_tanks_list[i] = neighbours_list[i]
    return count_potential_tanks, potential_tanks_list, count_assigned_tanks, assigned_tanks_list


def house_with_arrow_clean_nghb(values, house, print_flag):
    tot_len = total_length(values)
    count_pt, pt_list, count_at, at_list = control_tanks_around_house(values, house)
    if count_at == 1:
        for i in range(0, 4):
            if pt_list[i]:
                newvalue = values[pt_list[i]].replace(str(i), "")
                if print_flag == 'print':
                    print('####11 house:', house, '|square:', pt_list[i],
                          '(' + values[pt_list[i]] + ')' + ' |new value:', newvalue)
                values[pt_list[i]] = newvalue
    if print_flag == 'print':
        print('\nCHARACTERS REMOVED:', tot_len - total_length(values))
    return values


def assigned_tank_clean_neighb(values):
    "Strategy 11"
    tot_len = total_length(values)
    start_time = time.clock()
    a1, a2, a3, tanks_assigned, a4, a5 = count_symbol(values, values)
    for tank in tanks_assigned:
        neighb_list = find_neighbours(values, [tank], 'All', 'yes')[2]
        for square in neighb_list:
            if len(values[square]) > 1:
                print('tank', tank, "|neighbour square:", square, "|value:", values[square])
                values[square] = em
                print("|neighbour square:", square, "|value changed to:", values[square])
    print('\nCHARACTERS REMOVED:', tot_len - total_length(values))
    print("Time elapsed:", round(time.clock() - start_time, 3), "seconds")
    return values


### STRATEGIES ###

def eliminate_initial_not_tanks(values, print_flag):
    print("STRATEGY 3: Clean the sqares that can't be tanks, eliminate arrows")
    start_time = time.clock()
    tot_len = total_length(values)
    all_tanks_list, empties_list, noinfo_list, tanks_assigned, tanks_not_assigned, houses_list = count_symbol(
        values, values)
    squares_with_arrows = noinfo_list + tanks_not_assigned
    # eliminate tanks that can't be
    potential_tanks = find_neighbours(values, HOUSES, 'Cross', 'yes')[1]
    print("### Removing tanks that can't be ...")
    for square in values:
        if square not in potential_tanks:
            if square not in HOUSES and square not in empties_list:
                values[square] = em
                if print_flag == 'print':
                    print("Initial cleaning; square", square, "can't be a tank, assigned -")
    # now eliminate arrows that can't be
    print("### Removing arrows that can't be...")
    for sqarrow in squares_with_arrows:
        neighbours = find_neighbours_for_one_house(values, sqarrow, 'no')
        for i in range(0, 4):
            if neighbours[i]:  # neighbour will be empty '' if the value for it was '-'
                if len(values[neighbours[i]]) > 1 or values[neighbours[i]] == em:  ##7
                    if dict_nghb_rev[i] in values[sqarrow]:
                        # print(sqarrow, neighbours)
                        newvalue = values[sqarrow].replace(dict_nghb_rev[i], "")
                        if print_flag == 'print':
                            print('##7 square ' + sqarrow + ' (' + values[sqarrow] + ') |neighbour:',
                                  neighbours[i], '(' + values[neighbours[i]] + ')' + '|removing:',
                                  dict_nghb_rev[i], ' |new value:', newvalue)
                        values[sqarrow] = newvalue
            else:
                if dict_nghb_rev[i] in values[sqarrow]:
                    newvalue = values[sqarrow].replace(dict_nghb_rev[i], "")
                    if print_flag == 'print':
                        print('####8 square:', sqarrow, '(' + values[sqarrow] + ')' + ' |new value:', newvalue, \
                              'neighbour position:', i)
                    values[sqarrow] = newvalue
    print('\nCHARACTERS REMOVED:', tot_len - total_length(values))
    print("Time elapsed:", round(time.clock() - start_time, 3), "seconds")
    return values


def eliminate_empty_adj_unit(values):
    "STRATEGY 7"
    start_time = time.clock()
    tot_len = total_length(values)
    noinfo_list = count_symbol(values, values)[2]
    for square in noinfo_list:  # noinfo_list
        # check only adjacent units, not all units
        values_test = values.copy()
        values_test = assign_tank(values_test, square, '', '0123', '')
        nghbr_units = find_nghbr_units(square)
        for unit in nghbr_units:
            # difference, holes_list, holes_listing = count_sections_in_units(unit, values_test)
            difference, unit_new_value = difference_headers_tanks(unit, values_test)
            if difference < 0:  # removed:  and len(values_test[square]) > 1
                print('###12 unit:', unit[3], unit[0], '|diff:', difference, '|square:', square,
                      '|current value:', values[square], '|changed to:', em)
                values[square] = em
                values_test = values.copy()
    print('\nCHARACTERS REMOVED:', tot_len - total_length(values))
    print("Time elapsed:", round(time.clock() - start_time, 3), "seconds")
    return values


def clean_unit_sections_diff_zero(values, HOUSES):
    """STRATEGY 4"""
    for unit in unitlist:
        difference, holes_list, holes_listing = count_sections_in_units(unit, values)
        # assign tanks if difference =0
        if difference == 0:
            for hole in holes_listing:
                # TODO this can be optimized by changing 1,3,5,7... at once, same for even numbers
                if len(hole) in (1, 3, 5, 7, 9, 11, 13, 15, 17):  ##1
                    i = 1
                    while i <= len(hole):
                        print('##00 Assigned tank for square: ', hole[0], 'UNIT', unit[3], unit[0])
                        assign_tank(values, hole[i - 1], '', '0123',
                                    'print')  # former value: assign_tank(values, hole[i - 1])
                        i += 2
                if len(hole) in (2, 4, 6, 8, 10, 12, 14):  ##2
                    # print('##2 Hole with even number, starts with: ', hole[0],'unit',unit[3],unit[0],)
                    neighbours_set = find_neighbours(values, hole, 'Cross', 'yes')[1]
                    for square in neighbours_set:
                        if len(values[square]) > 1 and em in values[square]:
                            print('##2 Hole with even number, starts with: ', hole[0], 'unit', unit[3], unit[0], )
                            print('##2 changed square ', square, ' from ', values[square], ' to ', em)
                            values[square] = em

        # check for empties if difference =1
        if difference == 1:
            print('##4 Possible empty in adjacent unit: ', ' unit', unit[3], unit[0], )
    print('Nothing else can be solved.')
    return values


def solve_unit_diff_zero(values):
    "STRATEGY 10"
    for unit in unitlist:
        all_tanks_list, empties_list, noinfo_list, tanks_assigned, tanks_not_assigned, houses_list = count_symbol(
            values, values)
        difference = difference_headers_tanks(unit, values)[0]
        if difference == 0:
            for i in range(len(unit[2])):
                if unit[2][i] in noinfo_list:
                    # TODO, This is just one case of a slot in the middle; other cases should be considered too
                    # Like slot on the edge or slot with multiple squares
                    if i > 0 and i < len(unit[2]) - 1:  # -.- # if unit[2][i + 1] and unit[2][i - 1]: # -.-
                        if unit[2][i + 1] in empties_list and unit[2][i - 1] in empties_list:
                            print('##15 removing - symbol', unit[3], unit[0], unit[2][i], values[unit[2][i]])
                            new_val = values[unit[2][i]].replace('-', '')
                            values[unit[2][i]] = new_val
                            print('##15 after removal', unit[3], unit[0], unit[2][i], values[unit[2][i]])
                    if i > 0 and i < len(unit[2]) - 2:  # -.XX  # unit[2][i + 1] and unit[2][i + 2] and unit[2][i - 1]
                        if unit[2][i + 1] in houses_list and unit[2][i + 2] in houses_list \
                                and unit[2][i - 1] in empties_list:
                            print('##15 removing - symbol', unit[3], unit[0], unit[2][i], values[unit[2][i]])
                            new_val = values[unit[2][i]].replace('-', '')
                            values[unit[2][i]] = new_val
                            print('##15 after removal', unit[3], unit[0], unit[2][i], values[unit[2][i]])
                    if i > 1 and i < len(unit[2]) - 1:  # XX.-  # unit[2][i - 1] and unit[2][i - 2] and unit[2][i + 1]
                        if unit[2][i - 1] in houses_list and unit[2][i - 2] in houses_list \
                                and unit[2][i + 1] in empties_list:
                            print('##15 removing - symbol', unit[3], unit[0], unit[2][i], values[unit[2][i]])
                            new_val = values[unit[2][i]].replace('-', '')
                            values[unit[2][i]] = new_val
                            print('##15 after removal', unit[3], unit[0], unit[2][i], values[unit[2][i]])


def check_headers_tanks(values):
    for unit in unitlist:
        # cleaning unit if header=tanks ##3
        if int(unit[1]) == len(count_symbol(values, unit[2])[0]) and unit[4] != 'x':
            print("##3 Condition with tanks count met:", 'unit: ', unit[3], unit[0], 'flag:', unit[4])
            unitlist[unitlist.index(unit)][4] = 'x'
            print("Unit state changed to x for unit:", unit[3], unit[0])
            for square in unit[2]:
                if len(values[square]) > 1 and em in values[square]:
                    print('##3 Changed square ', square, ' from ', values[square], ' to ', em)
                    values[square] = em
    print('Nothing else can be solved.')
    return values


def house_direction(values):
    "STRATEGY 8"
    tot_len = total_length(values)
    for house in count_solved_houses(values, values)[1]:
        neighbours = find_neighbours_for_one_house(values, house, 'yes')
        count_pot_t, pot_t_list, count_ass_t, ass_t_list = control_tanks_around_house(values, house)
        if count_pot_t == 1 and count_ass_t == 0:  # Only 1 potential tank left
            for i in range(0, 4):
                if neighbours[i] and len(values[neighbours[i]]) > 1 and str(i) in values[neighbours[i]]:
                    print('house', house, 'no_of_candidates:', count_pot_t, '|square > tank:',
                          neighbours[i], 'value:', values[neighbours[i]])
                    print("##8 assignment of house to tank; house: ", house, '| tank:', neighbours[i],
                          'current value: ', values[neighbours[i]], 'new value: ', str(i))
                    assign_tank(values, neighbours[i], house, str(i), 'yes')
        if count_ass_t == 1 and count_pot_t > 0:  # tank assigned, but some potentials left
            for i in range(0, 4):
                if neighbours[i] and len(values[neighbours[i]]) > 1 and str(i) in values[neighbours[i]]:
                    print('##14 House:', house, '1 assigned tank + some potentials - removing potentials')
                    print('Removing potentials:', neighbours[i], 'value:', values[neighbours[i]])
                    values[neighbours[i]] = values[neighbours[i]].replace(str(i), '')
                    print('New value:', values[neighbours[i]])

                    # values[neighbours[i]] = str(i)
                    # else:
                    #    print('Something wrong. Candidate doesnt fit')
    print('\nCHARACTERS REMOVED:', tot_len - total_length(values))
    return values


def find_lonely_houses(values):
    "STRATEGY 6"
    tot_len = total_length(values)
    for house in HOUSES:
        count_pot_t, potential_tanks_list, count_ass_t, as3 = control_tanks_around_house(values, house)
        if count_pot_t == 1 and count_ass_t == 0:
            # print('house',house,'potential tanks list',potential_tanks_list)
            for i in range(0, 4):
                # empty candidates must be omitted
                if potential_tanks_list[i] and len(values[potential_tanks_list[i]]) > 1:
                    print('house', house, 'no_of_candidates', count_pot_t, 'house_to_be_treated', \
                          potential_tanks_list[i])
                    print("##8 assignment of house to tank; house: ", house, '| tank:', \
                          potential_tanks_list[i], 'current value: ', values[potential_tanks_list[i]], \
                          'new value:', str(i))
                    assign_tank(values, potential_tanks_list[i], house, str(i), 'print')
    print('\nCHARACTERS REMOVED:', tot_len - total_length(values))
    return values


def test_assign_tank_per_neighbour(values):
    "STRATEGY 11"
    tot_len = total_length(values)
    start_time = time.clock()
    # Level 1
    for house in count_solved_houses(values, values)[1]:  # count_solved_houses(values, values)[1]
        neighbours_list_wide = find_neighbours(values, [house], 'Wide', '')[0].get(house)
        houses_list_wide = []
        for square in neighbours_list_wide:
            if square in HOUSES:
                houses_list_wide.append(square)
        neighbours_list = find_neighbours_for_one_house(values, house, 'yes')
        i = 0
        for i in range(0, 4):
            if neighbours_list[i]:
                values_test = values.copy()
                values_test = assign_tank(values_test, neighbours_list[i], house, str(i), '')
                for h in houses_list_wide:  # originally in HOUSES
                    #  check only houses that are in distance of 3 squares from original square
                    count_pot_t = control_tanks_around_house(values_test, h)[0]
                    count_ass_t = control_tanks_around_house(values_test, h)[2]
                    if count_pot_t == 0 and count_ass_t == 0 and \
                                    str(i) in values[neighbours_list[i]]:
                        print('##9 WARNING DURING TEST: House without a tank')
                        print("Tested house:", house, "/ tank assigned at square:", neighbours_list[i],
                              'as a result there is a house without a tank', h)
                        print("Remove", str(i), 'from square', neighbours_list[i])
                        print("Current value", values[neighbours_list[i]])
                        newvalue = values[neighbours_list[i]].replace(str(i), "")
                        print('new value:', newvalue)
                        values[neighbours_list[i]] = newvalue
                        continue
                    elif count_pot_t == 1 and count_ass_t == 0:
                        for j in range(0, 4):
                            pot_t_list = control_tanks_around_house(values_test, h)[1]
                            if pot_t_list[j]:
                                values_test = assign_tank(values_test, pot_t_list[j], h, str(j), '')

    print('\nCHARACTERS REMOVED:', tot_len - total_length(values))
    print("Time elapsed:", round(time.clock() - start_time, 3), "seconds")
    return values


def main():
    global HOUSES
    values, HOUSES = grid_values(grid)
    global central
    central = 4  # for display function: how many characters per column
    choice = None
    while choice != "0":
        print()
        choice = input("Your choice - enter 1 for menu: ")  # What To Do ???
        print()

        if choice == "0":
            print("Good bye!\n")
        elif choice == "1":
            display(grid_values(grid)[0], 'short', central)
            print \
                ("""
            ---MENU---

            0  - Exit
            1  - Print initial grid
            2  - Display current state
            3  - Clean the sqares that can't be tanks, eliminate arrows [sets: -]
            4  - Compare unit header to number of sections [sets: o, -]
            5  - Compare unit header to number of tanks [sets: -]
            6  - Find lonely HOUSES [sets: o, -]
            7  - Eliminate empties in adjacent units [sets: -]
            8  - Identify tank direction by house options
            9  - test_assign_tank_per_neighbour
            10 - Solve unit when new diff=0
            11 - Assigned tanks - clean neighb
            12 - new unit test
            13 - clean neghb for houses
            90 - Display setting: input number of characters per column
            91 - Print current Values
            92 - Start from {values_copy}
            93 - Check if the puzzle is solved
            97 - Change square manually
            98 - Assign a tank manually
            99 - Reset
            """)
        elif choice == "2":
            stats(values)
        elif choice == "3":
            eliminate_initial_not_tanks(values, '')
        elif choice == "4":
            clean_unit_sections_diff_zero(values, HOUSES)
        elif choice == "5":
            check_headers_tanks(values)
        elif choice == "6":
            find_lonely_houses(values)
        elif choice == "7":
            eliminate_empty_adj_unit(values)
        elif choice == "8":
            house_direction(values)
        elif choice == "9":
            test_assign_tank_per_neighbour(values)
        elif choice == "10":
            solve_unit_diff_zero(values)
        elif choice == '11':
            assigned_tank_clean_neighb(values)
        elif choice == '12':
            difference_headers_tanks_solve(values)
        elif choice == '13':
            for house in HOUSES:
                house_with_arrow_clean_nghb(values, house, 'print')
        elif choice == "90":
            central = int(input("Enter number of characters for column in display; usually 3-6: "))
            stats(values)
        elif choice == "91":
            print(values)
        elif choice == '92':
            # rid=examples.eval(input("Select your snapshot: "))
            values = examples.a2.copy()
        elif choice == '93':
            check_if_solved(values, 'print')
        elif choice == "97":
            assigned_tank = ''
            assigned_value = ''
            while not assigned_tank and not assigned_value:
                assigned_tank = input(str("Type address of square in format XX.YY:  "))
                assigned_value = input(str("Type value like - or -5:  "))
            values[assigned_tank] = assigned_value
        elif choice == "98":
            assigned_tank = ''
            while assigned_tank not in squares:
                assigned_tank = input(str("Type address of square in format XX.YY: "))
            assign_tank(values, assigned_tank, '', '0123', 'print')  # former value:  assign_tank(values, assigned_tank)
        elif choice == "99":
            values = grid_values(grid)[0]
            print(display(values, '', central))
        else:
            print(" ### Wrong option ### ")


main()
