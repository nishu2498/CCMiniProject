"""
In a real life scenario this would be the "model" of the application.
"""
import json


def get_defaults():
    """
    Builds a dictionary with a few values. Check README.md for details.
    :return: dictionary with three "Car" objects.
    """
    _cars = dict()
    _cars["1"] = Car("1", "Ford", "Focus", 2012, 8000)
    _cars["2"] = Car("2", "Dacia", "Logan", 2006, 2400)
    _cars["3"] = Car("3", "BMW", "320d", 2010, 10100)
    return _cars


def get_cars():
    """Returns a JSON containing all the cars"""
    _cars = [_car.get_info() for _car in cars.values()]
    return json.dumps(_cars, sort_keys=True, indent=4)


def get_car(identifier):
    """
    Returns a JSON with details about a specific car
    :param identifier: the id of the car we're looking for
    :return: string, a JSON with the car's details or None if car does not exist
    """
    _car = cars.get(identifier)
    if _car is not None:
        return _car.jsonify()
    return None


def insert(car_info):
    """
    Adds car to current list of cars.
    :param car_info: dictionary containing all necessary details
    """
    identifier = car_info["id"]
    _car = Car(identifier,
               car_info["make"],
               car_info["model"],
               car_info["year"],
               car_info["price"])
    cars[identifier] = _car


def update(identifier, car_info):
    """
    Updates attributes of car identified by first parameter.
    :param identifier: id of the car to update
    :param car_info: dictionary containing all necessary attributes
    """
    _car = cars[identifier]
    _car.update_info(car_info)


def delete(identifier):
    """
    Deletes car from database
    :param identifier: id of the car to delete
    """
    del cars[identifier]


class Car:
    """Used to store information about each car"""

    def __init__(self, identifier, make, model, year, price):
        self.id = identifier
        self.make = make
        self.model = model
        self.year = year
        self.price = price

        # build a dictionary with all the values
        self.info_dict = dict()
        self.info_dict["id"] = self.id
        self.info_dict["make"] = self.make
        self.info_dict["model"] = self.model
        self.info_dict["year"] = self.year
        self.info_dict["price"] = self.price

    def update_info(self, new_info):
        """Replaces old attributes with new ones"""
        self.make = new_info["make"]
        self.model = new_info["model"]
        self.year = new_info["year"]
        self.price = new_info["price"]

        self.info_dict["make"] = new_info["make"]
        self.info_dict["model"] = new_info["model"]
        self.info_dict["year"] = new_info["year"]
        self.info_dict["price"] = new_info["price"]

    def get_info(self):
        """Returns a dictionary containing all the information about the car"""
        return self.info_dict

    def jsonify(self):
        """Returns a JSON representation of the object"""
        return json.dumps(self.info_dict, sort_keys=True, indent=4)


class CarList:
    pass
    # TODO: make this class


if __name__ == "__main__":
    # print defaults
    cars = get_defaults()
    for car in cars.values():
        print(car.jsonify())
else:
    # initialise "model"
    cars = get_defaults()
