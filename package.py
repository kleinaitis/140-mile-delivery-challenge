class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline_time, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline_time = deadline_time
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return (
            "Package ID: {}\n"
            "Address: {}\n"
            "City: {}\n"
            "State: {}\n"
            "Zipcode: {}\n"
            "Deadline Time: {}\n"
            "Weight: {}\n"
            "Delivery Time: {}\n"
            "Status: {}"
        ).format(
            self.ID,
            self.address,
            self.city,
            self.state,
            self.zipcode,
            self.deadline_time,
            self.weight,
            self.delivery_time,
            self.status
        )

    # Sets the status of the package based on the user input time
    def set_package_status(self, desired_time):
        if self.delivery_time is not None and self.delivery_time <= desired_time:
            self.status = "Delivered"
        elif self.departure_time is not None and self.departure_time <= desired_time:
            self.status = "En route"
        else:
            self.status = "At Hub"

    # Retrieves the status of the package based on the user input time
    def get_package_status(self, desired_time):
        self.set_package_status(desired_time)
        return self.status
