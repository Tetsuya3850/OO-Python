
from enum import Enum
from collections import deque
from abc import ABCMeta, abstractmethod


class Rank(Enum):
    RESPONDENT = 0
    MANAGER = 1
    DIRECTOR = 2


class Employee(metaclass=ABCMeta):
    def __init__(self, rank, callcenter):
        self.rank = rank
        self.callcenter = callcenter
        self.call = None

    def take_call(self, call):
        self.call = call
        self.call.respondent = self

    def call_completed(self):
        self.call = None
        self.callcenter.notify_completed_call(self)

    @abstractmethod
    def escalate_call(self):
        pass

    def _escalate_call(self):
        self.callcenter.notify_escalate_call(self.call)
        self.call = None


class Respondent(Employee):
    def __init__(self, callcenter):
        super().__init__(Rank.RESPONDENT, callcenter)

    def escalate_call(self):
        self.call.rank = Rank.MANAGER
        self._escalate_call()


class Manager(Employee):
    def __init__(self, callcenter):
        super().__init__(Rank.MANAGER, callcenter)

    def escalate_call(self):
        self.call.rank = Rank.DIRECTOR
        self._escalate_call()


class Director(Employee):
    def __init__(self, callcenter):
        super().__init__(Rank.DIRECTOR, callcenter)

    def escalate_call(self):
        raise NotImplementedError('Directors must be able to handle any call')


class Call:
    def __init__(self):
        self.rank = Rank.RESPONDENT
        self.respondent = None

    def request_escalation(self):
        self.respondent.escalate_call


class CallCenter:
    NUM_RESPONDENTS = 10
    NUM_MANAGERS = 3
    NUM_DIRECTORS = 1

    def __init__(self):
        self.respondents = [Respondent(self)
                            for _ in range(self.NUM_RESPONDENTS)]
        self.managers = [Manager(self) for _ in range(self.NUM_MANAGERS)]
        self.directors = [Director(self) for _ in range(self.NUM_DIRECTORS)]
        self.call_pool = deque()
        self.manager_pool = deque()
        self.director_pool = deque()

    def dispatch_call(self, call):
        for respondent in self.respondents:
            if respondent.call == None:
                respondent.take_call(call)
                return
        self.call_pool.append(call)

    def notify_escalate_call(self, call):
        if call.rank == Rank.MANAGER:
            for manager in self.managers:
                if manager.call == None:
                    manager.take_call(call)
                    return
            self.manager_pool.append(call)
        elif call.rank == Rank.DIRECTOR:
            for director in self.directors:
                if director.call == None:
                    director.take_call(call)
                    return
            self.director_pool.append(call)

    def notify_completed_call(self, employee):
        if employee.rank == Rank.RESPONDENT:
            next_call = self.call_pool.popleft()
        elif employee.rank == Rank.MANAGER:
            next_call = self.manager_pool.popleft()
        elif employee.rank == Rank.DIRECTOR:
            next_call = self.director_pool.popleft()
        if next_call:
            employee.take_call(next_call)
