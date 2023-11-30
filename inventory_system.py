class Inventory:

    def __init__(self):
        self.red_key = 0
        self.blue_key = 0

    def add_red(self):
        self.red_key += 1

    def minus_red(self):
        self.red_key -= 1

    def add_blue(self):
        self.blue_key += 1

    def minus_blue(self):
        self.blue_key -= 1

