# Sells three drinks. Coke, Sprite, Water.
# Each cost 1 (dollars)


from abc import ABCMeta, abstractmethod


class VendorMachine:
    CAPACITY_PER_DRINK = 10

    def __init__(self):
        self.drinks = []
        self.drinks.append([Coke(1) for _ in range(self.CAPACITY_PER_DRINK)])
        self.drinks.append([Sprite(1) for _ in range(self.CAPACITY_PER_DRINK)])
        self.drinks.append([Water(1) for _ in range(self.CAPACITY_PER_DRINK)])
        self.no_dollor_state = NoDollarState(self)
        self.has_dollor_state = HasDollarState(self)
        self.soldout_state = SoldoutState(self)
        self.state = self.no_dollor_state

    def insert_dollar(self):
        self.state.insert_dollar()

    def eject_dollar(self):
        self.state.eject_dollar()

    def choose_drink(self):
        return self.state.choose_drink()

    def release_drink(self, id):
        return self.drinks[id-1].pop()

    def show_availability(self):
        if self.drinks[0]:
            print('Coke available, set 1 to buy.')
        if self.drinks[1]:
            print('Sprite available, set 2 to buy.')
        if self.drinks[2]:
            print('Water available, set 3 to buy.')

    def is_sold_out(self):
        sold_out = True
        for drink in self.drinks:
            if drink:
                sold_out = False
        return sold_out


class State(metaclass=ABCMeta):
    def __init__(self, vendor):
        self.vendor = vendor

    def insert_dollar(self):
        pass

    def eject_dollar(self):
        pass

    def choose_drink(self):
        pass


class NoDollarState(State):
    def __init__(self, vendor):
        super().__init__(vendor)

    def insert_dollar(self):
        print("Dollar inserted")
        self.vendor.state = self.vendor.has_dollor_state


class HasDollarState(State):
    def __init__(self, vendor):
        super().__init__(vendor)

    def eject_dollar(self):
        print("Dollar Ejected")
        self.vendor.state = self.vendor.no_dollor_state

    def choose_drink(self):
        self.vendor.show_availability()
        choice = int(input())
        drink = self.vendor.release_drink(choice)
        if self.vendor.is_sold_out():
            self.vendor.state = self.vendor.soldout_state
        else:
            self.vendor.state = self.vendor.no_dollor_state
        return drink


class SoldoutState(State):
    def __init__(self, vendor):
        super().__init__(vendor)


class Drink:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost


class Coke(Drink):
    def __init__(self, cost):
        super().__init__('Coke', cost)


class Sprite(Drink):
    def __init__(self, cost):
        super().__init__('Sprite', cost)


class Water(Drink):
    def __init__(self, cost):
        super().__init__('Water', cost)


vendor = VendorMachine()
vendor.insert_dollar()
drink = vendor.choose_drink()
print(drink.name)