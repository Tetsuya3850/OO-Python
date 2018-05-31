
class StockData:
    def __init__(self):
        self.observers = []
        self.start = None
        self.end = None
        self.max = None
        self.min = None

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notity_observers(self):
        for observer in self.observers:
            observer.update()

    def update_data(self, start, end, max, min):
        self.start = start
        self.end = end
        self.max = max
        self.min = min
        self.notity_observers()


class StockDisplay:
    def __init__(self, stock_data):
        self.stock_data = stock_data
        stock_data.add_observer(self)

    def unsubscribe(self):
        self.stock_data.remove_observer(self)


class MaxMinStockDisplay(StockDisplay):
    def __init__(self, stock_data):
        super().__init__(stock_data)
        self.max = None
        self.min = None

    def update(self):
        self.max = self.stock_data.max
        self.min = self.stock_data.min
        self.display()

    def display(self):
        print("Stock max is {0}, min is {1}".format(self.max, self.min))


class StartEndStockDisplay(StockDisplay):
    def __init__(self, stock_data):
        super().__init__(stock_data)
        self.start = None
        self.end = None

    def update(self):
        self.start = self.stock_data.start
        self.end = self.stock_data.end
        self.display()

    def display(self):
        print("Stock start is {0}, end is {1}".format(self.start, self.end))


stock_data = StockData()
max_min_display = MaxMinStockDisplay(stock_data)
start_end_display = StartEndStockDisplay(stock_data)
stock_data.update_data(10, 20, 40, 10)
