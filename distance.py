# Ladd Gillies ID:010028835

from csv import reader
from datetime import timedelta

# Space-time - O(N^2)

# Read in csv file that has the names of all possible delivery locations
with open('WGUPS Distance  Names.csv') as csv_name_file:
    namesCSV = reader(csv_name_file, delimiter=',')
    namesCSV = list(namesCSV)

# Read in csv file that is the distances between locations
with open('WGUPS Distance Table.csv', encoding='utf-8-sig') as csvfile:
    distanceCSV = reader(csvfile, delimiter=',')
    distanceCSV = list(distanceCSV)

    # Method for checking the distance from one location to another and adds them up for a total that gets returned
    # Space-time - O(1)
    def check_distance(row, column, sum_of_distance):
        distance = distanceCSV[column][row]
        if distance == '':
            distance = distanceCSV[row][column]
        sum_of_distance += float(distance)
        return sum_of_distance

    # Method for getting the distance from one location to another.
    # Space-time - O(1)
    def get_distance(row, column):
        distance = distanceCSV[row][column]
        if distance == '':
            distance = distanceCSV[column][row]
        return float(distance)

    # Getter for the names file for address comparison
    # Space-time - O(1)
    def check_address():
        return namesCSV

    # Times trucks will leave the hub
    first_time_list = ['8:00:00']
    second_time_list = ['9:05:00']
    third_time_list = ['11:00:00']
    # Space-time - O(1)
    # Getter for all the trucks time lists - for calculating when each package was delivered based on what time the
    # truck left and how far the truck had to travel for the delivery

    def get_time_list(num):
        if num == 1:
            return first_time_list
        if num == 2:
            return second_time_list
        if num == 3:
            return third_time_list

    # Method for converting time into a datetime from string. take in time as a parameter and convert it into hours,
    # minutes and seconds and return the converted time
    # Space-time - O(1)
    def time_convert(time):
        (h, m, s) = time.split(':')
        time = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        return time

    # Method for checking the time. Get the truck number and the distance the truck has travelled.
    # Adds up the sum for each truck
    # Space-time - O(N)
    def check_time(num, distance):
        distance_time = distance / 18
        convert = '{0:02.0f}:{1:02.0f}'.format(*divmod(distance_time * 60, 60))
        delivery_time = convert + ':00'
        get_time_list(num).append(delivery_time)
        sums = timedelta()
        for count in get_time_list(num):
            sums += time_convert(count)
        return sums

    # these lists represent the sorted trucks that are put in order of efficiency in the function below
    truck_one = []
    truck_two = []
    truck_three = []
    truck_one_distance = []
    truck_two_distance = []
    truck_three_distance = []

    # Greedy Algorithm
    # The space-time complexity of this algorithm is O(N^2). This is due to the two for loops and the repeated lookup
    # functionality required to determine the lowest possible path then move the truck to that position.
    # Space-time - O(N^2)
    def greedy_algorithm(truck_distance_list, truck_number, current_location):
        if len(truck_distance_list) == 0:
            return truck_distance_list
        else:
            try:
                lowest_value = 20.0
                next_location = 0
                for index in truck_distance_list:
                    if get_distance(current_location, int(index[1])) <= lowest_value:
                        lowest_value = get_distance(current_location, int(index[1]))
                        next_location = int(index[1])
                for i in truck_distance_list:
                    if get_distance(current_location, int(i[1])) == lowest_value:
                        get_trucks(truck_number).append(i)
                        get_truck_distance(truck_number).append(i[1])
                        value = truck_distance_list.index(i)
                        truck_distance_list.pop(value)
                        current_location = next_location
                        greedy_algorithm(truck_distance_list, truck_number, current_location)
            except ValueError:
                pass

    # Insert 0 (Hub) in to the index for each truck, as it is where they start and end their journey
    truck_one_distance.insert(0, '0')
    truck_two_distance.insert(0, '0')
    truck_three_distance.insert(0, '0')

    # Getter for all the trucks package list
    # Space-time - O(1)
    def get_trucks(num):
        if num == 1:
            return truck_one
        if num == 2:
            return truck_two
        if num == 3:
            return truck_three

    # Getter for all the truck distance lists
    # Space-time - O(1)
    def get_truck_distance(num):
        if num == 1:
            return truck_one_distance
        if num == 2:
            return truck_two_distance
        if num == 3:
            return truck_three_distance
