
import datetime


class Day:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        self.available = set()
        self.available.add((10, 17))

    def book_if_available(self, start, end):
        match = None
        for timespan in self.available:
            if timespan[0] <= start < end <= timespan[1]:
                match = timespan
        if match:
            self.available.remove(match)
            if match[0] < start:
                self.available.add((match[0], start))
            if match[1] > end:
                self.available.add((end, match[1]))
            return True
        else:
            return False


class Service:
    def __init__(self):
        year, month, day = str(datetime.date.today()).split('-')
        self.week = [Day(int(year), int(month), int(day)+i)
                     for i in range(1, 7)]

    def show_availability(self):
        for i in range(len(self.week)):
            day = self.week[i]
            print("ID: {0} In {1}, {2}, {3}, we are available at {4}".format(i,
                                                                             day.year, day.month, day.day, day.available))

    def request_booking(self):
        self.show_availability()
        print("What day are you looking for? Choose by ID")
        id = int(input())
        print("When do you want to start?")
        start = int(input())
        print("When do you want to end?")
        end = int(input())
        if not 0 <= id < len(self.week) or start < 10 or end > 17 or start > end:
            print("Invalid input! Try again!")
            self.request_booking()
        result = self.week[id].book_if_available(start, end)
        if result:
            print("Booked!")
        else:
            print("Sorry, that time was just taken. Want to try another time? Yes or No.")
            again = input()
            if again.lower() == 'yes':
                self.request_booking()


service = Service()
service.request_booking()
service.show_availability()