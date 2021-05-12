# This programme has states in the form of functions.
# Each state returns the transition if any(if not then returns None).
# the return values of fuctions are list if any input is to be given to next state.
# the 2nd element of the list is inputs to be given to it.


# Declaring some global variables.
counter = 0
curr_values = {'A1':0, 'A2':0, 'B1':0, 'B2':0, 'C1':0, 'C2':0, 'D1':0, 'D2':0}
possible_pairs = {
    'A1' : ['A2', 'B1', 'C2'],
    'A2' : ['A1', 'B2', 'D1'],
    'B1' : ['A1', 'B2', 'D2'],
    'B2' : ['A2', 'B1', 'C1'],
    'C1' : ['C2', 'D1', 'A2'],
    'C2' : ['C1', 'B1', 'D2'],
    'D1' : ['D2', 'B2', 'C1'],
    'D2' : ['A1', 'D1', 'C2']
}
t = None


# Takes the input of the user and adds it to the cars dictionary.
def cars_arriving():
    cars = input("Cars arrived : ")
    counter = 0
    for road in curr_values:
        curr_values[road] += int(cars[counter])
        counter += 1
    return find_max_traffic


# checks the counter to determine if to take the input.
# Also controls when to exit the loop.
def check_counter():
    global counter
    counter += 1
    if counter <= t:
        return cars_arriving
    elif sum(curr_values.values()) != 0:
        return find_max_traffic
    else:
        print("Zero traffic left\nExiting...")
        return None


# finds the road on which the maximum number of cars.
def find_max_traffic():
    m_t_val = 0
    for road in curr_values:
        if curr_values[road]> m_t_val:
            m_t_val = curr_values[road]
            m_t_road = road
    return [find_optimum_signals, m_t_road]


# Finds the maximum road that can be opened
# along with opening the current road.
def find_optimum_signals(m_t_road):
    max_traffic = -1
    for road2 in possible_pairs[m_t_road]:
        if curr_values[road2] > max_traffic:
            max_traffic = curr_values[road2]
            m_t_road2 = road2
    return [execute, [m_t_road, m_t_road2]]


# OPens the signals for the current cycle.
# Prints the corresponding message.
def execute(operation):
    msgs = {'1':"go straight", '2':"go right"}
    operation = [x for x in operation if curr_values[x] != 0]
    print(f"Time Step: {counter}")
    print("signals to open fo this cycle are:")
    print("all other signals are off.")
    if len(operation)==2 and operation[0][0]==operation[1][0]:
        print(f"{operation[0][0]} : {msgs['1']}, {msgs['2']}")
    else:
        for x in operation:
            print(f"{x[0]} : {msgs[x[1]]}")
    print("currently standing cars : ", end = ' ')
    for x in curr_values:
        if x in operation:
            curr_values[x] -= 1
        print(curr_values[x], end = ' ')
    print()
    return check_counter


if __name__ == "__main__":
    t = int(input("Enter t : "))
    next = check_counter()

    # loop goes through all the directed states and calls the next function.
    while True:
        if next == None:
            break
        elif type(next) == list:
            next = next[0](next[1])
        else:
            next = next()