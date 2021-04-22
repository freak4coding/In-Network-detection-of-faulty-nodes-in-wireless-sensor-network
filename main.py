import decimal
import math
import statistics
from random import seed, randint, randrange

import matplotlib.pyplot as plt
from termcolor import colored

reading = []
xCoordinates = []
yCoordinates = []
neigbourTable = []
coorelationTable = []
Rank = []
voteTable = []
deviation = []
med = []
faulty_nodes = []
fault_free_nodes = []


def generateReading():
    seed(1)
    for i in range(0, 50):
        value = float(decimal.Decimal(randrange(2400, 2600)) / 100)
        reading.append(value)


def generateCoordinates():
    seed(1)
    for i in range(71):
        value = randint(1, 100)
        if value not in xCoordinates:
            xCoordinates.append(value)

    for i in range(89):
        value = randint(1, 100)
        if value not in xCoordinates:
            yCoordinates.append(value)

    print(colored("\n\nX-Coordinates : ", 'red', attrs=['bold']))
    for i in range(50):
        if i % 10 == 0:
            print()
        else:
            print(xCoordinates[i], end=" ")

    print(colored("\n\nY-Coordinates : ", 'red', attrs=['bold']))
    for i in range(50):
        if i % 10 == 0:
            print()
        else:
            print(yCoordinates[i], end=" ")


def plot_graph_for_nodes():
    c = 1
    faulty_Xcoordinates = []
    faulty_Ycoordinates = []
    # plotting the points
    plt.plot(xCoordinates, yCoordinates, color='black', linestyle=' ', linewidth=1,
             marker='o', markerfacecolor='yellow', markersize=20)

    for i in faulty_nodes:
        faulty_Xcoordinates.append(xCoordinates[i])
        faulty_Ycoordinates.append(yCoordinates[i])

    plt.plot(faulty_Xcoordinates, faulty_Ycoordinates, color='black', linestyle=' ', linewidth=1,
             marker='o', markerfacecolor='red', markersize=20)

    # labeling all nodes
    for i in range(50):
        plt.annotate(c, (xCoordinates[i] - 1, yCoordinates[i] - 1))
        c += 1

    # setting x and y axis range
    plt.ylim(1, 100)
    plt.xlim(1, 100)

    # naming the x axis
    plt.xlabel('x - coordinates')
    # naming the y axis
    plt.ylabel('y - coordinates')

    # giving a title to my graph
    plt.title('Faulty Nodes are Red and Fault free nodes are yellow')

    # function to show the plot
    plt.show()


def generateDistanceTable():
    for i in range(0, 50):
        a = []
        for j in range(0, 50):
            xdiff = abs(xCoordinates[j] - xCoordinates[i])
            ydiff = abs(yCoordinates[j] - yCoordinates[i])
            distance = int(math.sqrt(pow(xdiff, 2) + pow(ydiff, 2)))
            if distance <= 50 and distance != 0:  # Assuming transmission range to 50.0
                a.append(1)
            else:
                a.append(0)
        neigbourTable.append(a)

    print(colored("\n======================= Neighbour Table ==========================", 'green', attrs=['bold']))
    for i in range(0, 50):
        for j in range(0, 50):
            print(neigbourTable[i][j], end="   ")
        print()


def findCoorelation(a, b):
    x = a * b
    y = pow(a, 2) + pow(b, 2) - (a * b)
    return x / y


def coorelation():
    for i in range(0, 50):
        a = []
        for j in range(0, 50):
            if neigbourTable[i][j] == 1:
                a.append(round(findCoorelation(reading[i], reading[j]), 4))
            else:
                a.append(0.0)
        coorelationTable.append(a)


def corelationSum(a):
    summation = 0
    for i in range(0, 50):
        if neigbourTable[a][i] == 1:
            summation += coorelationTable[a][i]
    return summation


def transitonProbability(a, b):
    return coorelationTable[a][b] / (corelationSum(a) - coorelationTable[a][b])


def sensorRank():
    for i in range(0, 50):
        Rank.append(1)
    for i in range(0, 50):
        a = 0
        for j in range(50):
            if neigbourTable[i][j] == 1:
                a += Rank[j] * transitonProbability(j, i)
        Rank[i] = round(a, 4)


def vote(sensorIndex, neiIndex):
    if coorelationTable[sensorIndex][neiIndex] >= 0.50:
        return Rank[neiIndex]
    else:
        return -Rank[neiIndex]


def createVoteTable():
    #code for creating vote table
    for i in range(0, 50):
        a = []
        for j in range(0, 50):
            if neigbourTable[i][j] == 1:
                a.append(vote(i, j))
            else:
                a.append(0)
        voteTable.append(a)

    #code for printing vote table !!
    print("\n\n", colored('=============================================', 'green', attrs=['bold']), end="")
    print(colored(' VOTE TABLE ', 'blue', attrs=['bold']), end="")
    print(colored('=================================================', 'green', attrs=['bold']))
    for i in range(0, 50):
        for j in range(0, 50):
            print(voteTable[i][j], end="    ")
        print()


def find_Sn_Deviation():
    for i in range(0, 50):
        a = []
        for j in range(0, 50):
            if neigbourTable[i][j] == 1:
                a.append(voteTable[i][j])
        # print("list for median : ", a)
        med.append(round(statistics.median(a), 4))
    print()
    print("median : ", med)
    # print("overall median : ", round(statistics.median(med), 4))
    print("Sn :", round(1.1926 * statistics.median(med), 4))


def fault_checker():
    Sn = round(1.1926 * statistics.median(med), 4)
    for i in range(50):
        dev = Sn - med[i]
        if dev < -6 or dev > 2:
            faulty_nodes.append(i)
        else:
            fault_free_nodes.append(i)

    print(colored("faulty Nodes : ", 'red', attrs=['bold']))
    print(faulty_nodes)


def making_nodes_faulty(a):
    seed(1)
    for i in range(a):
        ind = randint(0, 49)
        value = float(decimal.Decimal(randrange(7000, 8000)) / 100)
        reading[ind] = value


if __name__ == '__main__':

    generateReading()
    a = int(input("Enter Fault percentage : "))
    making_nodes_faulty(int((50*a)/100))

    print(colored("Sensor's Reading : ", 'green', attrs=['bold']))
    for i in range(50):
        if i % 10 == 0:
            print()
        else:
            print(reading[i], end=" ")

    generateCoordinates()
    generateDistanceTable()
    print("\n\n========== ========== Coorelation Table ========== ==========")
    coorelation()
    for i in range(0, 50):
        for j in range(0, 50):
            print(coorelationTable[i][j], end="    ")
        print()

    sensorRank()
    print("\n\n", colored('Sensor Rank : ', 'red', attrs=['bold']), end="")
    print(Rank)

    createVoteTable()

    print()

    find_Sn_Deviation()

    fault_checker()

    plot_graph_for_nodes()