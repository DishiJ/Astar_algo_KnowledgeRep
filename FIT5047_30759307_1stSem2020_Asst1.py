import argparse as ap

import re

import platform

import pandas as pd

import copy



######## RUNNING THE CODE ####################################################

#   You can run this code from terminal by executing the following command

#   python planpath.py <INPUT/input#.txt> <OUTPUT/output#.txt> <flag>

#   for example: python planpath.py INPUT/input2.txt OUTPUT/output2.txt 0

#   NOTE: THIS IS JUST ONE EXAMPLE INPUT DATA

###############################################################################





################## YOUR CODE GOES HERE ########################################
class node:         # creating class node
    def __init__(self , id):
        self.id = id
        self.f = 0.0
        self.g = 0
        self.h = 0
        self.child = []
        self.parent = []
        self.path=''
        self.node_operator = 'S'
        self.nid = 'N' + self.id




# function to find the operator to go from current node till node
def operator_find(node_x,node_y,cur_node_x,cur_node_y):
    if node_x==cur_node_x-1 and node_y == cur_node_y :
        operator = 'U'
    elif node_x==cur_node_x-1 and node_y == cur_node_y+1:
        operator = 'RU'
    elif node_x==cur_node_x and node_y == cur_node_y+1:
        operator = 'R'
    elif node_x==cur_node_x+1 and node_y== cur_node_y+1:
        operator = 'RD'
    elif node_x==cur_node_x+1 and node_y== cur_node_y:
        operator = 'D'
    elif node_x==cur_node_x+1 and node_y== cur_node_y-1:
        operator = 'LD'
    elif node_x==cur_node_x and node_y== cur_node_y-1:
        operator = 'L'
    elif node_x==cur_node_x-1 and node_y== cur_node_y-1:
        operator = 'LU'
    else:
        operator = None
    return operator


def find_path_from_start(curr_node):    # function to find path from start till current node
    path_from_start_lst = []
    while (len(curr_node.parent) != 0):
        path_from_start_lst.append(curr_node.node_operator)
        curr_node = curr_node.parent[0]

    return path_from_start_lst


def list_to_string(path_from_list):     # converting the list containing operators to a string
    path_from_start_string = "S-"
    for i in path_from_list[::-1]:
        path_from_start_string = path_from_start_string + i + '-'

    return path_from_start_string[:-1]




def graphsearch(map, flag):     # function to find best path from start to goal node in map
    n = (len(map.index)) # n is the length or dimension of map dataframe
    for i in map.index:
        for j in map:
            if map.loc[i, j] == 'S':
                start_id = str(i) + str(j) # finding the start_id contining indexes where "S" is present in map

    for i in map.index:
        for j in map:
            if map.loc[i, j] == 'G':
                final_id = str(i) + str(j) # finding the final_id contining indexes where "G" is present in map

    start_node = node(start_id)  # creating a object of class type node with id as start_id
    start_node.h = ((int(final_id[0]) - int(start_node.id[0])) ** 2 + (
            int(final_id[1]) - int(start_node.id[1])) ** 2) ** 0.5  # calculating the h value using heuristic function
    start_node.f = start_node.g + start_node.h # f value as the sum of g and h
    current_node = start_node # creating a current_node as the start_node

    open_lst = [] # list to store ids of node that are in open state
    closed_lst = [] # list to store ids of nodes that are in closed state
    open_lst.append(current_node)
    count = 1
    count_closed = 1
    while (len(open_lst) > 0): # running the loop till open_lst is empty


        open_lst.sort(key=lambda x: (x.f, x.g))
        current_node = open_lst.pop(0) # removing the current_node from open list
        if current_node.id == final_id:
            reversed_path = find_path_from_start(current_node)
            straight_path_list = reversed_path[::-1]  # storing final path from start to goal in a list
            output_write_list = []
            current_x = int(start_id[0])  # current x coordinate as the first index of start_id
            current_y = int(start_id[1])  # current y coordinate as the second index of start_id
            current_node_output = start_node
            list_of_list = []
            list_of_list = [int(current_node_output.id[0]), int(current_node_output.id[1]), current_node_output.g,
                            current_node_output.node_operator]  # storing x,y,g,operator of current node
            output_write_list.append(list_of_list)

            for i in straight_path_list:
                if i == 'R':
                    current_x = current_x
                    current_y = current_y + 1
                elif i == 'D':
                    current_x = current_x + 1
                    current_y = current_y
                elif i == 'RD':
                    current_x = current_x + 1
                    current_y = current_y + 1
                elif i == 'L':
                    current_x = current_x
                    current_y = current_y - 1
                elif i == 'U':
                    current_x = current_x - 1
                    current_y = current_y
                elif i == 'RU':
                    current_x = current_x - 1
                    current_y = current_y + 1
                elif i == 'LD':
                    current_x = current_x + 1
                    current_y = current_y - 1
                elif i == 'LU':
                    current_x = current_x - 1
                    current_y = current_y - 1

                for c in current_node_output.child:  # looping inside the child list of current node
                    if c.id == str(current_x) + str(current_y):
                        # if current x y coordinates same as a child's id, making child as current node
                        current_node_output = c

                list_of_list = []
                list_of_list = [current_x, current_y, current_node_output.g, current_node_output.node_operator]
                output_write_list.append(list_of_list)

            output_string = ""
            string_to_pycharm = ""
            for i in output_write_list:
                new_df = copy.deepcopy(map)  # creating a copy of map into new_df
                new_df.iloc[i[0], i[1]] = '*'  # replacing current node's value by * in new_df

                output_string = output_string + i[3] + "-"  # appending the operator of current node
                string_df = new_df.to_string(index=False)  # converting dataframe to string
                list_df = string_df.split('\n')
                list_df_final = list_df[1:]
                new_string = '\n'.join(some.replace(' ', '') for some in list_df_final)
                string_to_pycharm = string_to_pycharm + new_string + "\n" + "\n" + "\n"

                if str(i[0]) + str(i[1]) == final_id:
                    break
                else:
                    # appending the g value of current node to the string
                    string_to_pycharm = string_to_pycharm + output_string[:-1] + " " + str(i[2]) + "\n" + "\n" + "\n"
                    # print(output_string[:-1] + " " + str(i[2]))

            string_to_pycharm = string_to_pycharm + output_string[:-1] + "-G " + str(
                output_write_list[-1][2]) + "\n" + "\n"
            solution = string_to_pycharm  # returning the final string containing output to solution variable
        else :
            if (flag > 0):  # for console output
                check_node = current_node
                current_string = ""
                f_path_list = find_path_from_start(check_node)
                f_path_string = list_to_string(f_path_list)  # finding the path from start to current_node
                current_string = check_node.nid + ":" + f_path_string + " " + check_node.node_operator + " " + str(
                    count) + " " + str(round(check_node.g, 3)) + " " + str(round(check_node.h, 3)) + " " + str(
                    round(check_node.f, 3))
                print(current_string)
                count = count + 1

            closed_lst.append(current_node)  # adding to the closed list the node with minimum f value
            if (flag > 0):
                count_closed = 1
                closed_string = ""
                for closed_objct in closed_lst:  # iterating through the nodes in closed list
                    f_path_list = find_path_from_start(closed_objct)
                    f_path_string = list_to_string(f_path_list)  # finding the path from start to current_node
                    closed_string = closed_string + "(" + closed_objct.nid + ":" + " " + closed_objct.node_operator + " " + \
                                    str(count_closed) + " " + str(round(closed_objct.g, 3)) + " " + \
                                    str(round(closed_objct.h, 3)) + " " + str(round(closed_objct.f, 3)) + ")" + ","
                    count_closed = count_closed + 1
                print("CLOSED : {" + closed_string[:-1] + "}")
            x = int(current_node.id[0])  # storing the first index as x coordinate of the current node
            y = int(current_node.id[1])  # storing the second index as y coordinate of the current node

            if map.loc[x, y] == 'G':  # if x and y coordinate matches "G" in the map, then goal is reached
                break
            else:

                neighbour_lst = []  # creating empty neighbour list to find neighburs of current node
                for i, j in [[x - 1, y], [x - 1, y + 1], [x, y + 1], [x + 1, y + 1], [x + 1, y], [x + 1, y - 1],
                             [x, y - 1], [x - 1, y - 1]]:  # check for boundary conditions in map
                    if i >= 0 and j >= 0 and i < n and j < n:
                        a = str(i) + str(j)
                        neighbour_lst.append(a)  # valid neighbours based on boundary appended to neighbour list
                neighbour_lst2 = neighbour_lst.copy()

                for i in neighbour_lst2:

                    if map.loc[int(i[0]), int(i[1])] == 'X':
                        x_x = int(i[0])  # storing x coordinate where "X" found in neighbours
                        y_y = int(i[1])  # storing y coordinate where "X" found in neighbours
                        x2 = int(current_node.id[0])
                        y2 = int(current_node.id[1])
                        op = operator_find(x_x, y_y, x2, y2)

                        if op == 'R' or op == 'L':
                            x3 = x_x - 1  # x coordinate of position above "X"
                            y3 = y_y  # y coordinate of position above "X"
                            x4 = x_x + 1  # x coordinate of position below "X"
                            y4 = y_y  # y coordinate of position below "X"
                            d = str(x3) + str(y3)
                            d2 = str(x4) + str(y4)
                            if d in neighbour_lst2:
                                try:

                                    neighbour_lst.remove(d)  # removing adjacent positions of "X"
                                except ValueError:
                                    pass
                            if d2 in neighbour_lst2:  # removing adjacent positions of "X"
                                try:

                                    neighbour_lst.remove(d2)

                                except ValueError:
                                    pass
                        elif op == 'U' or op == 'D':
                            x3 = x_x  # x coordinate of position left of "X"
                            y3 = y_y - 1  # y coordinate of position left of "X"
                            x4 = x_x  # x coordinate of position right of "X"
                            y4 = y_y + 1  # y coordinate of position right of "X"
                            d = str(x3) + str(y3)
                            d2 = str(x4) + str(y4)
                            if d in neighbour_lst2:
                                try:

                                    neighbour_lst.remove(d)  # removing adjacent positions of "X"
                                except ValueError:
                                    pass
                            if d2 in neighbour_lst2:
                                try:

                                    neighbour_lst.remove(d2)  # removing adjacent positions of "X"

                                except ValueError:
                                    pass

                        try:
                            neighbour_lst.remove(i)  # removing positions of "X" from neighbour list

                        except ValueError:
                            pass

                    for j in open_lst:
                        if j.id == i:
                            try:
                                neighbour_lst.remove(
                                    i)  # removing already present nodes in open list from neighbour list
                            except ValueError:
                                pass

                    for j in closed_lst:
                        if j.id == i:
                            try:
                                neighbour_lst.remove(
                                    i)  # removing already present nodes in closed list from neighbour list
                            except ValueError:
                                pass

                for i in neighbour_lst:  # final created neighbour list with valid nodes
                    new_node = node(i)  # new nodes created of class node
                    op = operator_find(int(new_node.id[0]), int(new_node.id[1]), int(current_node.id[0]),
                                       int(current_node.id[1]))
                    if op == 'U' or op == 'R' or op == 'D' or op == 'L':
                        new_node.g = 2  # new_node's g value of most recent move stored as 2 if not a diagonal move
                    elif op == 'RU' or op == 'RD' or op == 'LD' or op == 'LU':
                        new_node.g = 1  # new_node's g value of most recent move stored as 1 if diagonal move

                    new_node.parent.append(current_node)  # new created node's parent set as current node
                    current_node.child.append(new_node)  # current node's parent set as new created node

                    open_lst.append(new_node)  # appending the new node's created in open list

                    new_node.path = current_node.id + '-' + op + "-"
                    new_node.node_operator = op  # setting the new node's operator
                    # setting the new node g value as its own g value plus g value of its parent node
                    new_node.g = new_node.g + new_node.parent[0].g
                    distance = ((int(final_id[0]) - int(new_node.id[0])) ** 2 + (
                            int(final_id[1]) - int(new_node.id[1])) ** 2) ** 0.5  # heuristic distance
                    new_node.h = distance
                    new_node.f = new_node.g + new_node.h  # f taken as sum of g and h

                if flag > 0:  # for console output

                    check_node = current_node
                    child_string = ""
                    for objct in check_node.child:
                        f_path_list = find_path_from_start(objct)
                        f_path_string = list_to_string(f_path_list)  # finding path of current node from start node
                        child_string = child_string + objct.nid + ":" + f_path_string + " " + objct.node_operator + ","
                    print("Children : {" + child_string[:-1] + "}")

                if (flag > 0):  # for console output
                    open_string = ""
                    for open_objct in open_lst:
                        f_path_list = find_path_from_start(open_objct)
                        f_path_string = list_to_string(f_path_list)  # finding path of current node from start node
                        open_string = open_string + "(" + open_objct.nid + ":" + f_path_string + " " + \
                                      open_objct.node_operator + " " + str(round(open_objct.g, 3)) + " " + \
                                      str(round(open_objct.h, 3)) + " " + str(round(open_objct.f, 3)) + ")" + ","

                    print("OPEN : {" + open_string[:-1] + "}")
                    flag = flag - 1
        if solution == "":
            solution = "No Path Found"

return solution



def read_from_file(file_name):

    file_handle = open(file_name)
    read_file = file_handle.read()   # storing the entire content of file in string read_file
    n = int(read_file[0])               # n is the first character of the string giving the dimension of map
    input_string = read_file[1:].split("\n")[1:n+1]
    list1 = []
    list2 = []
    for i in input_string:      # creating list of list
        for j in i:
            list2.append(j)     # list2 contains row wise data to be inputted in the data frame
        list1.append(list2)     # list1 contains all the list2s
        list2 = []
    map = pd.DataFrame(list1)    # map is a data frame
    return map





###############################################################################

########### DO NOT CHANGE ANYTHING BELOW ######################################

###############################################################################



def write_to_file(file_name, solution):

    file_handle = open(file_name, 'w')

    file_handle.write(solution)



def main():

    # create a parser object

    parser = ap.ArgumentParser()



    # specify what arguments will be coming from the terminal/commandline

    parser.add_argument("input_file_name", help="specifies the name of the input file", type=str)

    parser.add_argument("output_file_name", help="specifies the name of the output file", type=str)

    parser.add_argument("flag", help="specifies the number of steps that should be printed", type=int)

    # parser.add_argument("procedure_name", help="specifies the type of algorithm to be applied, can be D, A", type=str)





    # get all the arguments

    arguments = parser.parse_args()



##############################################################################

# these print statements are here to check if the arguments are correct.

#    print("The input_file_name is " + arguments.input_file_name)

#    print("The output_file_name is " + arguments.output_file_name)

#    print("The flag is " + str(arguments.flag))

#    print("The procedure_name is " + arguments.procedure_name)

##############################################################################



    # Extract the required arguments



    operating_system = platform.system()



    if operating_system == "Windows":

        input_file_name = arguments.input_file_name

        input_tokens = input_file_name.split("\\")

        if not re.match(r"(INPUT\\input)(\d)(.txt)", input_file_name):

            print("Error: input path should be of the format INPUT\input#.txt")

            return -1



        output_file_name = arguments.output_file_name

        output_tokens = output_file_name.split("\\")

        if not re.match(r"(OUTPUT\\output)(\d)(.txt)", output_file_name):

            print("Error: output path should be of the format OUTPUT\output#.txt")

            return -1

    else:

        input_file_name = arguments.input_file_name

        input_tokens = input_file_name.split("/")

        if not re.match(r"(INPUT/input)(\d)(.txt)", input_file_name):

            print("Error: input path should be of the format INPUT/input#.txt")

            return -1



        output_file_name = arguments.output_file_name

        output_tokens = output_file_name.split("/")

        if not re.match(r"(OUTPUT/output)(\d)(.txt)", output_file_name):

            print("Error: output path should be of the format OUTPUT/output#.txt")

            return -1



    flag = arguments.flag

    # procedure_name = arguments.procedure_name





    try:

        map = read_from_file(input_file_name) # get the map

    except FileNotFoundError:

        print("input file is not present")

        return -1

    # print(map)



    solution_string = "" # contains solution



    solution_string = graphsearch(map, flag)

    write_flag = 1



    # call function write to file only in case we have a solution

    if write_flag == 1:

        write_to_file(output_file_name, solution_string)



if __name__ == "__main__":

    main()