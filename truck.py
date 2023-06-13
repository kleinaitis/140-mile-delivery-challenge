class Truck:
    def __init__(self, max_capacity, speed, assigned_packages, mileage, address, depart_time):
        self.max_capacity = max_capacity
        self.speed = speed
        self.assigned_packages = assigned_packages
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time

    def __str__(self):
        package_details = "\n".join(
            ["Package ID: {}, Status: {}".format(package.ID, package.status) for package in self.assigned_packages]
        )
        return (
            "Max Capacity: {}\n"
            "Speed: {}\n"
            "Mileage: {}\n"
            "Address: {}\n"
            "Departure Time: {}\n"
            "Assigned Packages:\n{}"
        ).format(
            self.max_capacity,
            self.speed,
            self.mileage,
            self.address,
            self.depart_time,
            package_details
        )
