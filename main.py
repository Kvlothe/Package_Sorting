# Ladd Gillies ID:010028835

from package import total_distance
from package import locate_package
from package import print_packages


# Main class - only for display of the command line interface and intake of input.
# All input is sent as parameters to other methods
# Space-time - O(N^2)
class Main:
    total_distance()
    choice = input("'l' or 'locate' to check by a package by time\n"
                   "'ts' or 'timestamp' to see all packages at a time\n"
                   "'e' or 'exit to quit: ")
    while choice != 'e' or choice != 'exit':
        if choice == 'l' or choice == 'locate':
            num = input('ID: ')
            time = input('Time (Military time: HH:MM:SS): ')
            locate_package(int(num), str(time))
        elif choice == 'ts' or choice == 'timestamp':
            ts_time = input('Time (Military time: HH:MM:SS): ')
            print_packages(ts_time)
        elif choice == 'e' or choice == 'exit':
            exit()
