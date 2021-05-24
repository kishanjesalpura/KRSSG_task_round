# This programme has states in the form of functions.
# 3(or 4) states can be defined here they are
#   1st : finding the optimum signal
#   2nd : changing the signals and according to the output given by finding optimum signals
#   3rd : executing the signals(i.e. changing vahicles list acc to current signals and also making the signals go off)
#   (4th : I don't think this might be considered as a state its the input to be taken from the user) 

# Declaring some global variables.
counter = 1
curr_values = {'A1':0, 'A2':0, 'B1':0, 'B2':0, 'C1':0, 'C2':0, 'D1':0, 'D2':0}
curr_signals = {'A1':False, 'A2':False, 'B1':False, 'B2':False, 'C1':False, 'C2':False, 'D1':False, 'D2':False}
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
    cars = input("\tCars arrived : ")
    counter = 0
    for road in curr_values:
        curr_values[road] += int(cars[counter])
        counter += 1


# finds the road on which the maximum number of cars.
def find_max_traffic():
    m_t_val = 0
    for road in curr_values:
        if curr_values[road]> m_t_val:
            m_t_val = curr_values[road]
            m_t_road = road
    return find_optimum_signals(m_t_road)


# Finds the maximum road that can be opened
# along with opening the current road.
def find_optimum_signals(m_t_road):
    max_traffic = -1
    for road2 in possible_pairs[m_t_road]:
        if curr_values[road2] > max_traffic:
            max_traffic = curr_values[road2]
            m_t_road2 = road2
    return m_t_road, m_t_road2

# takes in input the roads it has to open and prints the message of opening that roads 
# i.e. it executes or changes the signal accordingly
def change_signals(rds_to_open):
    for rd in rds_to_open:
        curr_signals[rd] = True
    lst = ["A", "B", "C", "D"]
    print("timestamp :", counter)
    print("\tcars present currently : ", list(curr_values.values()))
    for x in range(0,8,2):
        msg = ""
        val = list(curr_signals.values())
        if val[x] and val[x+1]:
            msg = "go straight, go right"
        elif val[x]:
            msg = "go straight"
        elif val[x+1]:
            msg = "go right"
        else:
            msg = "off"
        print("\t", lst[x//2], ":", msg)


# Once the signal is opened and the cars passed by then this fuction changes the counts in cars list
def  change_current_cars():
    for x in curr_signals:
        if curr_signals[x] == True:
            curr_values[x] -= 1
        curr_signals[x] = False
    print("\tcars present :", list(curr_values.values()))


if __name__ == "__main__":
    t = int(input("Enter t : "))
    
    for _ in range(t):
        cars_arriving()
        rds_to_open = find_max_traffic()
        change_signals(rds_to_open)
        change_current_cars()
        counter+=1
    while sum(curr_values.values()) != 0:
        rds_to_open = find_max_traffic()
        change_signals(rds_to_open)
        change_current_cars()
        counter+=1
    print("All traffic succesfully handled\nExiting the server.")
