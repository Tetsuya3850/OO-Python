
import random
from collections import deque
from enum import Enum


class Operation(Enum):
    IDLE = 0
    UP = 1
    DOWN = 2


class User:
    def __init__(self, floor):
        self.floor = floor
        self.dest = None

    def choose_direction(self):
        UP_OR_DOWN = input()
        return UP_OR_DOWN

    def choose_dest(self, elevator):
        dest = int(input())
        self.dest = dest
        elevator.add_request(dest)

    def arrive(self, floor):
        self.floor = floor
        self.dest = None


class Floor:
    def __init__(self, floor, manager):
        self.floor = floor
        self.manager = manager
        self.up_users = []
        self.up_request = False
        self.down_users = []
        self.down_request = False

    def enter_floor(self, user):
        print("Choose UP or DOWN")
        if user.choose_direction() == 'UP':
            self.up_users.append(user)
            if not self.up_request:
                self.up_request = True
                self.manager.elevator_request(self.floor, Operation.UP)
        else:
            self.down_users.append(user)
            if not self.down_request:
                self.down_request = True
                self.manager.elevator_request(self.floor, Operation.DOWN)

    def arrival(self, elevator):
        print("Which floor to go?")
        if elevator.state == Operation.UP:
            for user in self.up_users:
                user.choose_dest(elevator)
                elevator.passangers.append(user)
            self.up_users = []
            self.up_request = False
        else:
            for user in self.down_users:
                user.choose_dest(elevator)
                elevator.passangers.append(user)
            self.down_users = []
            self.down_request = False


class Elevator:
    def __init__(self, floor, manager):
        self.floor = floor
        self.manager = manager
        self.state = Operation.IDLE
        self.passangers = set()
        self.stops = set()

    def init_request(self, dest, direction):
        self.floor = dest
        self.manager.notify_arrival(self)
        self.state = direction
        if self.state == Operation.UP:
            self.move_up()
        else:
            self.move_down()

    def add_request(self, dest):
        self.stops.add(dest)

    def move_up(self):
        self.floor += 1
        if self.floor in self.stops:
            self.manager.notify_arrival(self)
            for passanger in self.passangers:
                if passanger.dest == self.floor:
                    passanger.arrive(self.floor)
                    self.passangers.remove(passanger)
            self.stops.remove(self.floor)
        if self.stops:
            self.move_up()
        else:
            self.state = Operation.IDLE
            self.manager.notify_idle(self)

    def move_down(self):
        self.floor -= 1
        if self.floor in self.stops:
            self.manager.notify_arrival(self)
            for passanger in self.passangers:
                if passanger.dest == self.floor:
                    passanger.arrive(self.floor)
                    self.passangers.remove(passanger)
            self.stops.remove(self.floor)
        if self.stops:
            self.move_down()
        else:
            self.state = Operation.IDLE
            self.manager.notify_idle(self)


class Manager:
    def __init__(self):
        self.num_floors = 10
        self.num_elevators = 3
        self.num_users = 5
        self.elevators = []
        self.floors = []
        self.pooled_requests = deque()

        for _ in range(self.num_elevators):
            elevator = Elevator(random.randint(1, self.num_floors), self)
            self.elevators.append(elevator)

        for i in range(1, self.num_floors+1):
            floor = Floor(i, self)
            self.floors.append(floor)

        for i in range(self.num_users):
            self.floors[0].enter_floor(User(1))

    def elevator_request(self, floor, direction):
        candid = None
        for elevator in self.elevators:
            if elevator.state == Operation.IDLE:
                if not candid or abs(elevator.floor - floor) < abs(candid.floor - floor):
                    candid = elevator
            elif elevator.state == Operation.UP and direction == Operation.UP:
                if floor >= elevator.floor:
                    if not candid or abs(elevator.floor - floor) < abs(candid.floor - floor):
                        candid = Elevator
            elif elevator.state == Operation.DOWN and direction == Operation.DOWN:
                if floor <= elevator.floor:
                    if not candid or abs(elevator.floor - floor) < abs(candid.floor - floor):
                        candid = Elevator
        if not candid:
            self.pooled_requests.append((floor, direction))
        else:
            if candid.state == Operation.IDLE:
                candid.init_request(floor, direction)
            else:
                candid.add_request(floor)

    def notify_arrival(self, elevator):
        self.floors[elevator.floor-1].arrival(elevator)

    def notify_idle(self, elevator):
        if self.pooled_requests:
            floor, direction = self.pooled_requests.popleft()
            elevator.init_request(floor, direction)
