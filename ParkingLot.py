# Parking for Cars and Bikes
# 3F with 10 slots each
# 2 bike spots and 8 car spots. Bike can stop on cart spot.

from enum import Enum


class VehicleSize(Enum):
    BIKE = 0
    CAR = 1


class Vehicle:
    def __init__(self, size, parkinglot):
        self.size = size
        self.parkinglot = parkinglot
        self.spot = None

    def request_spot(self):
        self.parkinglot.find_spot(self)

    def leave_spot(self):
        self.spot.vehicle = None
        self.spot = None


class Bike:
    def __init__(self, parkinglot):
        super().__init__(VehicleSize.BIKE, parkinglot)


class Car(Vehicle):
    def __init__(self, parkinglot):
        super().__init__(VehicleSize.CAR, parkinglot)


class Spot:
    def __init__(self, size):
        self.size = size
        self.vehicle = None


class Floor:
    num_car_spots = 8
    num_bike_spots = 2

    def __init__(self):
        self.car_spots = [Spot(VehicleSize.CAR)
                          for _ in range(self.num_car_spots)]
        self.bike_spots = [Spot(VehicleSize.BIKE)
                           for _ in range(self.num_bike_spots)]

    def find_spot(self, car):
        if car.size == VehicleSize.CAR:
            for spot in self.car_spots:
                if spot.vehicle == None:
                    return spot
        elif car.size == VehicleSize.BIKE:
            for spot in self.bike_spots:
                if spot.vehicle == None:
                    return spot
        return None


class ParkingLot:
    num_floors = 3

    def __init__(self):
        self.floors = [Floor() for _ in range(self.num_floors)]

    def find_spot(self, car):
        for floor in self.floors:
            spot = floor.find_spot(car)
            if spot:
                spot.vehicle = car
                car.spot = spot
            return
        print('Sorry, parking lot is full!')
        return None
