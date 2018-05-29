
import random
from collections import deque
from enum import Enum
from threading import Timer


class Direction(Enum):
    IDLE = 0
    UP = 1
    DOWN = 2


class User:
    def __init__(self, floor, elevator_manager):
        self.floor = floor
        self.elevator_manager = elevator_manager
        self.request_direction = None
        self.request_floor = None
        self.onboard = None

    def request_elevator(self):
        print("Choose up or down")
        UP_OR_DOWN = input()
        if UP_OR_DOWN.upper() == 'UP':
            self.request_direction = Direction.UP
        else:
            self.request_direction = Direction.DOWN
        self.elevator_manager.receive_request(self)

    def notify_pick_up(self, elevator):
        self.onboard = elevator
        print("Which floor would you like to go?")
        floor = int(input())
        self.request_floor = floor
        self.onboard.move()

    def notify_arrival(self):
        print("Arrived!")
        self.floor = self.request_floor
        self.onboard = None
        self.request_floor = None
        self.request_direction = None


class Elevator:
    def __init__(self, floor, elevator_manager):
        self.floor = floor
        self.elevator_manager = elevator_manager
        self.state = Direction.IDLE
        self.dest = None
        self.passanger = None

    def start_pick_up(self, user):
        self.dest = user.floor
        if self.floor <= user.floor:
            self.state = Direction.UP
        else:
            self.state = Direction.DOWN
        timer = Timer(abs(self.floor - self.dest), self.pick_up, (user, ))
        timer.start()

    def pick_up(self, user):
        self.floor = self.dest
        self.dest = None
        self.state = user.request_direction
        self.passanger = user
        self.passanger.notify_pick_up(self)

    def move(self):
        self.dest = self.passanger.request_floor
        timer = Timer(
            abs(self.floor - self.dest), self.arrive)
        timer.start()

    def arrive(self):
        self.floor = self.passanger.request_floor
        self.passanger.notify_arrival()
        self.dest = None
        self.passanger = None
        self.state = Direction.IDLE
        self.elevator_manager.notify_idle(self)


class ElevatorManager:
    def __init__(self):
        self.num_elevators = 3
        self.elevators = []
        for _ in range(self.num_elevators):
            elevator = Elevator(random.randint(1, 10), self)
            self.elevators.append(elevator)
        self.pooled_users = deque()

    def receive_request(self, user):
        candid = None
        for elevator in self.elevators:
            if elevator.state == Direction.IDLE:
                if not candid or abs(elevator.floor - user.floor) < abs(candid.floor - user.floor):
                    candid = elevator
        if not candid:
            print('pooled!')
            self.pooled_users.append(user)
        else:
            candid.start_pick_up(user)

    def notify_idle(self, elevator):
        if self.pooled_users:
            waiting_user = self.pooled_users.popleft()
            elevator.start_pick_up(waiting_user)


elevator_manager = ElevatorManager()
user = User(1, elevator_manager)
user.request_elevator()
