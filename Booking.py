
import datetime
from uuid import uuid4
from collections import defaultdict
from operator import itemgetter


class Reservation:
    def __init__(self, timestamp, name, start, end):
        self.id = str(uuid4())
        self.timestamp = timestamp
        self.name = name
        self.start = start
        self.end = end


class Day:
    def __init__(self, year, month, day, start_time, end_time):
        self.year = year
        self.month = month
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.available = [True for _ in range(end_time - start_time)]

    def book_if_available(self, start, end):
        for i in range(start-self.start_time, end-self.start_time):
            if not self.available:
                return False
        for i in range(start-self.start_time, end-self.start_time):
            self.available[i] = False
        return True

    def recover_availability(self, start, end):
        for i in range(start-self.start_time, end-self.start_time):
            self.available[i] = True


class Service:
    START_TIME = 10
    END_TIME = 17

    def __init__(self):
        timestamp = str(datetime.date.today())
        year, month, day = list(map(int, timestamp.split('-')))
        self.week = defaultdict()
        for i in range(1, 7):
            new_timestamp = "-".join([str(year), str(month), str(day+i)])
            self.week[new_timestamp] = Day(
                year, month, day+i, self.START_TIME, self.END_TIME)
        self.books = defaultdict()

    def show_availability(self):
        for timestamp, day in self.week.items():
            print("In {0} we are available at {1}".format(
                timestamp, day.available))

    def request_booking(self):
        self.show_availability()
        print("Hi, what is your name?")
        name = input()
        print("What day are you looking for? Choose day")
        day = input()
        print("When do you want to start?")
        start = int(input())
        print("When do you want to end?")
        end = int(input())
        if day not in self.week or start < self.START_TIME or end > self.END_TIME or start > end:
            print("Invalid input! Try again!")
            self.request_booking()
        result = self.week[day].book_if_available(start, end)
        if result:
            new_reservation = Reservation(day, name, start, end)
            self.books[new_reservation.id] = new_reservation
            print("Booked! Here is your reservation id. {0}".format(
                new_reservation.id))
        else:
            print("Sorry, that time was just taken.")

    def cancel_booking(self):
        print("What was your reservation id?")
        id = input()
        if id not in self.books:
            print("It seems you have not booked!")
            return
        reservation = self.books[id]
        self.week[reservation.timestamp].recover_availability(
            reservation.start, reservation.end)
        del self.books[id]
        print("Canceled!")

    def next_day(self):
        timestamp = str(datetime.date.today())
        year, month, day = list(map(int, timestamp.split('-')))
        format_timestamp = "-".join([str(year), str(month), str(day)])
        if format_timestamp in self.week:
            del self.week[format_timestamp]
        next_timestamp = "-".join([str(year), str(month), str(day+6)])
        self.week[next_timestamp] = Day(
            year, month, day+6, self.START_TIME, self.END_TIME)


service = Service()
service.request_booking()
service.show_availability()
service.cancel_booking()
service.show_availability()
