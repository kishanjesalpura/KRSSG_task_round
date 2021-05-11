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

def input_and_modifier():
    global counter
    counter -= 1
    cars_arrived = list(input("\ncars arriving : ").strip())
    y = 0
    for x in curr_values.keys():
        curr_values[x] += int(cars_arrived[y])
        y+=1
    print("\nCars waiting are : ", end="")
    for x in curr_values.values():
        print(x, end=" ")
    print('\n')


def max_signal(timecycle=1):
    if counter>0:
        input_and_modifier()
    val = 0
    name = []
    for n in curr_values:
        if curr_values[n]>val:
            name = [n]
            val = curr_values[n]
        elif curr_values[n]==val:
            name.append(n)
    move_decider(name, timecycle)


def move_decider(name_list, timecycle):
    tot_val = 0
    operation = []
    for x in name_list:
        for y in possible_pairs[x]:
            if curr_values[x]+curr_values[y] > tot_val:
                operation = [x, y]
                tot_val = curr_values[x]+curr_values[y]
    signal_printer(operation, timecycle)


def signal_printer(operation, timecycle):
    signals = {'A' : "A", 'B' : "B", 'C' : "C", 'D' : "D"}
    msgs = {'1':" ; go straight", '2':" ; go right"}
    operation = [x for x in operation if curr_values[x] != 0]
    for x in operation:
        curr_values[x] -= 1
        signals[x[0]] += msgs[x[1]]
    
    print("Timecycle : ", timecycle)
    for y in signals.values():
        if len(y)==1:
            print(y, "; off")
        else:
            print(y)
    print("final values : ", end=' ')
    cars_left = 0
    for x in curr_values.values():
        print(x, end=" ")
        cars_left+=x
    print('\n')
    if cars_left!=0:
        max_signal(timecycle+1)
    

if __name__ == "__main__":
    counter = int(input("Enter the number of inputs: "))
    max_signal()
