# Created by Jeff Kleinaitis (Student ID: #010286686)

import csv
import datetime
import truck
from package import Package

from hashtable import HashTable

package_hash_table = HashTable()


# Uses CSV data to create package objects and inserts them into the specified hash table
# Space-Time Complexity = O(n) where n is the number of packages in the CSV
def import_packages_from_csv(filename, hash_table):
    # Opens and reads the CSV file/data - O(n)
    with open(filename) as package_info:
        package_data = csv.reader(package_info)

        # Iterates over each package in the CSV file and creates new - O(1)
        for parcel in package_data:
            parcel_id = int(parcel[0])
            parcel_address = parcel[1]
            parcel_city = parcel[2]
            parcel_state = parcel[3]
            parcel_zipcode = parcel[4]
            parcel_deadline_time = parcel[5]
            parcel_weight = parcel[6]
            parcel_delivery_status = "At Hub"

            # Creates a package object using the extracted information from the CSV - 0(1)
            parcel = Package(parcel_id, parcel_address, parcel_city, parcel_state, parcel_zipcode,
                             parcel_deadline_time, parcel_weight, parcel_delivery_status)

            # Inserts package object into the hash table - O(1)
            hash_table.insert(parcel_id, parcel)


# Uses provided CSV file from WGU to create package objects
import_packages_from_csv('ProjectCSVs/Package_Information.csv', package_hash_table)


# Retrieves distance between two addresses based on the CSV provided by WGU.
def get_distance_between_addresses(x_value, y_value):
    with open("ProjectCSVs/Address_Distances.csv") as csvfile:
        distance_data = csv.reader(csvfile)
        distance_matrix = list(distance_data)

    if x_value == -1 or y_value == -1:
        return 0.0

    # Uses distance matrix to calculate the distance between the x and y value
    distance = float(distance_matrix[x_value][y_value] or distance_matrix[y_value][x_value])

    return distance


# Uses provided address to return corresponding address ID, or -1 if no match is found in the CSV.
def get_address_id(address):
    with open("ProjectCSVs/Delivery_Addresses.csv", encoding='utf-8-sig') as csvfile:
        address_data = csv.reader(csvfile)
        for row in address_data:
            if row[2].find(address) != -1:
                return int(row[0])
    return -1


# Assigns variables for the hub address, max truck capacity, and truck speed
wgups_hub_address = "4001 South 700 East"
truck_capacity = 16
truck_speed = 18

# Defines packages and start times for trucks
trucks_data = [
    {
        'packages': [1, 4, 8, 13, 14, 15, 16, 19, 20, 21, 30, 34, 39, 40],
        'start_time': datetime.datetime.combine(datetime.date.today(), datetime.time(hour=8, minute=0))
    },
    {
        'packages': [3, 6, 7, 9, 11, 12, 18, 25, 26, 28, 29, 31, 32, 36, 37, 38],
        'start_time': datetime.datetime.combine(datetime.date.today(), datetime.time(hour=9, minute=5))
    },
    {
        'packages': [2, 5, 10, 17, 22, 23, 24, 27, 33, 35],
        'start_time': datetime.datetime.combine(datetime.date.today(), datetime.time(hour=10, minute=20))
    },
]

trucks = []

# Creates truck objects based on the defined data
for data in trucks_data:
    truck_obj = truck.Truck(truck_capacity, truck_speed, data['packages'], 0, wgups_hub_address,
                            data['start_time'])
    trucks.append(truck_obj)

# Assigns variables to each specific truck
wgups_truck1 = trucks[0]
wgups_truck2 = trucks[1]
wgups_truck3 = trucks[2]
wgups_trucks = [wgups_truck1, wgups_truck2, wgups_truck3]


# Calculates total mileage for a list of trucks
# Space-Time Complexity: O(n) where n is the number of trucks in the list
def get_total_mileage(truck_list):
    total_mileage = sum(t.mileage for t in truck_list)
    return total_mileage


# Looks up and displays package details
# Space-Time Complexity: O(1)
def lookup_package_details(pkg_id, table, desired_time):
    # Looks up package within the hash table based on the package id - O(1)
    p = table.lookup_value(pkg_id)

    # If package is found, calls display_package_info to display the details of the package - O(1)
    if p:
        p.set_package_status(desired_time)
        display_package_info(pkg_id, {
            "address": p.address,
            "deadline_time": p.deadline_time,
            "city": p.city,
            "zipcode": p.zipcode,
            "weight": p.weight,
            "status": p.status,
            "time": p.delivery_time.strftime("%I:%M %p"),
        }, desired_time)
    else:
        print("Package not found.")


# Calculates optimal delivery route for a WGUPS truck using a "nearest neighbor" algorithm
# Updates package details as packages are delivered by a truck
# Space-Time Complexity: O(n^2 log n)
def calculate_optimal_delivery_route(wgups_truck, hash_table):
    undelivered_packages = []

    # Gathers a list of undelivered packages from the truck's assigned package list.
    # O(n) where n is the number of assigned packages
    for pkg_id in wgups_truck.assigned_packages:
        pkg = hash_table.lookup_value(pkg_id)
        if pkg and pkg not in undelivered_packages:
            undelivered_packages.append(pkg)

    wgups_truck.assigned_packages.clear()
    departure_time = wgups_truck.depart_time

    # Space-Time Complexity: O(n) where n is the number of packages
    while undelivered_packages:
        # Gets the current address ID of the truck
        current_address_id = get_address_id(wgups_truck.address)

        # Sorts undelivered packages based on the distance to their addresses (descending order)
        # Space-Time Complexity: Python's built-in sort function has a time complexity of O(n log n)
        undelivered_packages.sort(
            key=lambda p: get_distance_between_addresses(current_address_id, get_address_id(p.address)), reverse=True)

        # Delivers the nearest package from the undelivered packages list
        nearest_package = undelivered_packages.pop()
        shortest_distance = get_distance_between_addresses(current_address_id, get_address_id(nearest_package.address))

        # Updates truck's assigned packages, mileage, and address as package is delivered
        wgups_truck.assigned_packages.append(nearest_package.ID)
        wgups_truck.mileage += shortest_distance
        wgups_truck.address = nearest_package.address
        nearest_package.departure_time = departure_time

        # Calculates and updates truck's travel time as it delivers the package
        travel_time = shortest_distance / 18
        wgups_truck.time += datetime.timedelta(hours=travel_time)

        # Sets the delivery time of the delivered package
        nearest_package.delivery_time = wgups_truck.time


calculate_optimal_delivery_route(wgups_truck1, package_hash_table)
calculate_optimal_delivery_route(wgups_truck2, package_hash_table)
calculate_optimal_delivery_route(wgups_truck3, package_hash_table)


# Displays a formatted menu to the user
def display_menu(display_option_0, display_option_1, display_option_2, display_option_3, display_option_4=None,
                 display_option_5=None):
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print(f"┃{display_option_0:^50}  ┃")
    print("┃                                                    ┃")
    print(f"┃{display_option_1:^50}  ┃")
    print("┃                                                    ┃")
    print(f"┃{display_option_2:^50}  ┃")
    print("┃                                                    ┃")
    print(f"┃{display_option_3:^50}  ┃")
    if display_option_4 is not None:
        print("┃                                                    ┃")
        print(f"┃{display_option_4:^50}  ┃")
    if display_option_5 is not None:
        print("┃                                                    ┃")
        print(f"┃{display_option_5:^50}  ┃")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")


# Displays information about a package at the user's specified time.
def display_package_info(pkg_id, package_info, desired_time):
    print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print(f"┃               Package #{pkg_id} at {desired_time.strftime('%I:%M %p')}               ┃")
    print("┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃")
    print(f"┃ Package ID:          {str(pkg_id):<29} ┃")
    print(f"┃ Delivery Address:    {package_info['address']:<29} ┃")
    print(f"┃ Delivery Deadline:   {package_info['deadline_time']:<29} ┃")
    print(f"┃ Delivery City:       {package_info['city']:<29} ┃")
    print(f"┃ Delivery Zip Code:   {package_info['zipcode']:<29} ┃")
    print(f"┃ Package Weight:      {package_info['weight']:<29} ┃")
    print(f"┃ Delivery Status:     {package_info['status']:<29} ┃")
    if package_info['status'] not in ["En route", "At Hub"]:
        print(f"┃ Delivery Time:       {package_info['time']:<29} ┃")
    print("┃                                                    ┃")
    print("┃ Press Enter to Return to the Main Menu...          ┃")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")


def main():
    # Space-Time Complexity: O(n) where n is the number of packages in the hash table, and trucks in the truck list.
    while True:
        # Displays the main menu
        display_menu("Package Tracking System", "1. Display Package Information (Specified Time)",
                     "2. Display Package Information (Delivery Time)", "3. Display Total Mileage", "4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            # Prompts user for package ID (or blank for all) and specified time
            parcel_id = input("\nEnter the package ID or leave blank to display all packages: ")
            desired_time = input("\nEnter the desired time (format: HH:MM AM/PM): ")

            try:
                # Converts the user specified time into datetime format
                user_entered_time = datetime.datetime.strptime(desired_time, "%I:%M %p").time()
                todays_date = datetime.date.today()
                desired_time = datetime.datetime.combine(todays_date, user_entered_time)

            except ValueError:
                print("\nInvalid time format. Please use the format HH:MM AM/PM (e.g., 10:00 AM)")
                continue

            if parcel_id == '':
                # If package ID is blank, the program prints the package ID and status for all packages
                # O(n) where n is the number of packages
                package_status_list = []
                for bucket in package_hash_table.table:
                    for key_value_pair in bucket:
                        parcel_id, parcel = key_value_pair
                        package_status = parcel.get_package_status(desired_time)
                        if package_status is not None:
                            package_status_list.append((parcel_id, package_status))

                package_status_list.sort(key=lambda x: x[0])
                print("\nPackage ID  |  Delivery Status")
                for parcel_id, package_status in package_status_list:
                    print(f"{parcel_id:^11} |  {package_status:^16}")
                print("\nPress Enter to Return to the Main Menu...")
                input()
            else:
                try:
                    # If package ID was entered, looks up and displays package details for specified package ID
                    lookup_package_details(int(parcel_id), package_hash_table, desired_time)
                    input()
                except ValueError:
                    print("\nInvalid package ID. Please try again.")
        elif choice == "2":
            # Lookup and print delivery information for each package in each truck
            for i, each_truck in enumerate(wgups_trucks, start=1):
                for package_id in each_truck.assigned_packages:
                    package = package_hash_table.lookup_value(int(package_id))
                    print(f"Truck {i} delivered Package {package.ID} at {package.address} at {package.delivery_time}")
            print("\nPress Enter to Return to the Main Menu...")
            input()
        elif choice == "3":
            # Displays the total mileage, and rounded individual mileage for each truck
            # O(n) where n is the number of trucks to iterate through
            display_menu(f"Total Mileage Traveled: {round(get_total_mileage(trucks), 1)}",
                         f"Truck 1: {round(wgups_truck1.mileage, 1)}",
                         f"Truck 2: {round(wgups_truck2.mileage, 1)}",
                         f"Truck 3: {round(wgups_truck3.mileage, 1)}",
                         "Press Enter to Return to the Main Menu...")
            input()
        elif choice == "4":
            # Exits the program
            print("\nExiting the program...")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
