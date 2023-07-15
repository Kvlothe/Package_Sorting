# Ladd Gillies ID:010028835

from distance import check_distance
from distance import get_distance
from distance import greedy_algorithm
from distance import check_address
from distance import get_truck_distance
from distance import check_time
from distance import get_trucks
from distance import time_convert
from hash import Hash
from csv import reader

# Space-time - O(N^2)

# Read in the package file that and making a list for easy manipulation and comparison.
with open('WGUPS Package File.csv', encoding='utf-8-sig') as csvfile:
    packages = reader(csvfile, delimiter=',')
    packages = list(packages)

    # Calls the Hashmap class to create an object of Hashmap
    delivery_hash = Hash()

    # Creates lists that will represent the trucks for delivery
    first_deliveries = []
    second_deliveries = []
    third_deliveries = []

    # Lists for my trucks that I will use to populate the distance lists with an optimized route
    truck_one = []
    truck_two = []
    truck_three = []

    # These lists are used for optimizing and getting the distance between routes.
    truck_one_distance = []
    truck_two_distance = []
    truck_three_distance = []

    # the times below represent the times that each truck leaves the hub
    # Each package will have a time they leave the hub attached
    first_time = '8:00:00'
    second_time = '9:05:00'
    third_time = '11:00:00'

    # Read in values from CSV file and insert them into key / item pairs
    # these values are what makes up the nested dictionary inside the Hash table
    # Space-time - O(N)
    for row in packages:
        package_ID = row[0]
        address = row[1]
        city = row[2]
        state = row[3]
        zip_code = row[4]
        deadline = row[5]
        mass = row[6]
        note = row[7]
        exodus = ''
        location = ''
        status = 'At hub'
        arrival = '00:00:00'
        key = package_ID
        item = [package_ID, location, address, city, state, zip_code, deadline, mass, note, exodus, status, arrival]

        # Sorting the packages on to the trucks. Based on the notes provided in the file,
        # each package is placed on to a truck.
        # some changes are made to  the read in data, as to make it easier for manipulation.
        # I would like to find a way of automating this process a bit more and not have it so restricted to this
        # particular file
        # inserts every package into a hashmap with a key and item pair
        if item[6] != 'EOD':
            if 'Must' in item[8] or '' in item[8]:
                first_deliveries.append(item)
        if item[6] == '10:30 AM':
            item[6] = '10:30:00'
        if item[6] == '9:00 AM':
            item[6] = '9:00:00'
        if item[0] == '19' or item[0] == '14':
            first_deliveries.append(item)
        if 'Can only be' in item[8]:
            second_deliveries.append(item)
        if 'Delayed' in item[8]:
            second_deliveries.append(item)
        if '84104' in item[5] and '10:30' not in item[6]:
            third_deliveries.append(item)
        if 'Wrong address listed' in item[8]:
            item[2] = '410 S State St'
            item[5] = '84111'
            third_deliveries.append(item)
        if item not in first_deliveries and item not in second_deliveries and item not in third_deliveries:
            if len(second_deliveries) > len(third_deliveries):
                third_deliveries.append(item)
            else:
                second_deliveries.append(item)
        delivery_hash.insert(key, item)

    # Getter for the hashmap that was created by the read in csv file
    # Space-time - O(1)
    def get_hash():
        return delivery_hash

    # Getter for all the trucks deliveries lists
    # Space-time - O(1)
    def get_deliveries(num):
        if num == 1:
            return first_deliveries
        if num == 2:
            return second_deliveries
        if num == 3:
            return third_deliveries

    # Getter for all trucks lists
    # Space-time - O(1)
    def fetch_trucks(num):
        if num == 1:
            return truck_one
        if num == 2:
            return truck_two
        if num == 3:
            return truck_three

    # Getter for all truck distance lists
    # Space-time O(1)
    def get_distances(num):
        if num == 1:
            return truck_one_distance
        if num == 2:
            return truck_two_distance
        if num == 3:
            return truck_three_distance

    # Getter for each truck departure time
    # Space-time O(1)
    def get_exodus(num):
        if num == 1:
            return first_time
        if num == 2:
            return second_time
        if num == 3:
            return third_time


# Method for adding the time that the package will leave the hub to each package. Sorted by which truck they are on
# Space-time O(N)
def exodus_time(num):
    e = 0
    for values in get_deliveries(num):
        get_deliveries(num)[e][9] = get_exodus(num)
        fetch_trucks(num).append(get_deliveries(num)[e])
        e += 1


# Calls for each truck to pass their packages through the time method, adds a time to the package to be used to compare
# against the users time to see where the package is.
exodus_time(1)
exodus_time(2)
exodus_time(3)


# Method for getting the locations for every package so easy searching of the distance table
# Adds the distances to a list to pass through the greedy algorithm for sorting for the shortest distance
# Space-time O(N^2)
def get_location(num):
    try:
        count = 0
        for a in fetch_trucks(num):
            for b in check_address():
                if a[2] == b[2]:
                    get_distances(num).append(b[0])
                    fetch_trucks(num)[count][1] = b[0]
                    break
            count += 1
    except IndexError:
        pass


# Calls for each truck to get the locations for all their packages
get_location(1)
get_location(2)
get_location(3)


# Method for calculating and checking the distance for each package to each location. returns the total
# distance for each truck. Prints out the last delivery of each truck and returns the total miles each truck drove
# Space-time O(N)
def distance_time(num):
    count = 0
    baron = 0
    for countess in range(len(get_truck_distance(num))):
        try:
            count = check_distance(int(get_truck_distance(num)[countess]), int(get_truck_distance(num)[countess + 1]), count)
            delivery = check_time(num, get_distance(int(get_truck_distance(num)[countess]), int(get_truck_distance(num)[countess + 1])))
            get_trucks(num)[baron][11] = str(delivery)
            last_delivery = delivery
            get_hash().update(int(get_trucks(num)[baron][0]), fetch_trucks(num))
            baron += 1
        except IndexError:
            pass
    print('Truck ', num, ' last delivery was at ', last_delivery)
    return count


# Calls for each truck to the greedy algorithm for package sorting
# Space-time - O(N^2)
greedy_algorithm(truck_one, 1, 0)
greedy_algorithm(truck_two, 2, 0)
greedy_algorithm(truck_three, 3, 0)

# Calls to the distance calculator for each truck
distance_truck_one = distance_time(1)
distance_truck_two = distance_time(2)
distance_truck_three = distance_time(3)


# Method for printing all the packages at a given time by the user
# Space-time O(N)
def print_packages(time):
    time = time_convert(time)
    for count in range(1, 41):
        departure = time_convert(get_hash().get(str(count))[9])
        arrivals = time_convert(get_hash().get(str(count))[11])
        print('Package ID: ' + get_hash().get(str(count))[0])
        print('Mass: ' + get_hash().get(str(count))[7])
        print('Destination: ' + get_hash().get(str(count))[2], ',' + get_hash().get(str(count))[3], ','
              + get_hash().get(str(count))[4], ',' + get_hash().get(str(count))[5])
        print('Deadline: ' + get_hash().get(str(count))[6])
        if time <= departure:
            print('Package at the hub.')
            print('Estimated delivery ' + str(arrivals), '\n')
        elif time >= departure and time >= arrivals:
            print('Delivered at: ' + str(arrivals), '\n')
        elif departure <= time < arrivals:
            print('Package en route to destination.')
            print('Estimated delivery ' + str(arrivals), '\n')


# Method for printing out a specific package at a given time
# Space-time O(1)
def locate_package(id_number, time):
    time = time_convert(time)
    exodus_time = time_convert(get_hash().get(str(id_number))[9])
    arrival_time = time_convert(get_hash().get(str(id_number))[11])
    print('ID: ' + get_hash().get(str(id_number))[0])
    print('Mass: ' + get_hash().get(str(id_number))[7])
    print('Destination: ' + get_hash().get(str(id_number))[2], ',' + get_hash().get(str(id_number))[3], ','
          + get_hash().get(str(id_number))[4], ',' + get_hash().get(str(id_number))[5])
    print('Deadline: ' + get_hash().get(str(id_number))[6])
    if time <= exodus_time:
        print('At Hub, leaves at ' + str(exodus_time))
        print('Estimated delivery ' + str(arrival_time), '\n')
    elif time >= exodus_time:
        print('Left the Hub at ' + str(exodus_time), '\n')
        if time <= arrival_time:
            print('En route')
            print('Estimated delivery ' + str(arrival_time), '\n')
        if time >= arrival_time:
            print('Delivered at ' + str(arrival_time), '\n')


# Method for printing the distances of each truck and the total distance driven by the WGUPS
# Space-time O(1)
def total_distance():
    total_distances = distance_truck_one + distance_truck_two + distance_truck_three
    print('Truck one drove ', "{0:.2f}".format(distance_truck_one), 'miles')
    print('Truck two drove ', "{0:.2f}".format(distance_truck_two), 'miles')
    print('Truck three drove ', "{0:.2f}".format(distance_truck_three), 'miles')
    print('For a total of : '"{0:.2f}".format(total_distances), 'miles')
