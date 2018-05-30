class Item:
    def __init__(self, name):
        self.name = name
        self.make()

    def make(self):
        print("Made {0}".format(self.name))


class Burger(Item):
    def __init__(self):
        super().__init__('Burger')


class Fries(Item):
    def __init__(self):
        super().__init__('Fries')


class Shake(Item):
    def __init__(self):
        super().__init__('Shake')


class Menu:
    def __init__(self):
        self.table = ['Burger', 'Fries', 'Shake']

    def add_menu(self, item):
        self.table.append(item)


class Order:
    def __init__(self, customer):
        self.customer = customer
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)


class Meal:
    def __init__(self, customer):
        self.customer = customer
        self.meal = []

    def add_food(self, food):
        self.meal.append(food)


class Customer:
    def __init__(self, waitress):
        self.waitress = waitress
        self.call_waitress()

    def call_waitress(self):
        self.waitress.take_order(self)

    def take_or_not(self):
        choice = input()
        return choice.upper() == "YES"

    def receive_meal(self, meal):
        for food in meal.meal:
            print("Yummy, {0}".format(food.name))


class Waitress:
    def __init__(self):
        self.menu = Menu()

    def take_order(self, customer):
        new_order = Order(customer)
        for item in self.menu.table:
            print("Would you like a {0}? Yes or No.".format(item))
            if customer.take_or_not():
                new_order.add_order(item)
        self.chef.order_up(new_order)

    def deliver(self, meal):
        meal.customer.receive_meal(meal)


class Chef:
    def __init__(self, waitress):
        self.waitress = waitress

    def order_up(self, new_order):
        new_meal = Meal(new_order.customer)
        for item in new_order.orders:
            if item == 'Burger':
                new_meal.add_food(Burger())
            elif item == 'Fries':
                new_meal.add_food(Fries())
            elif item == 'Shake':
                new_meal.add_food(Shake())
        self.waitress.deliver(new_meal)


waiteress = Waitress()
chef = Chef(waiteress)
waiteress.chef = chef
customer = Customer(waiteress)
