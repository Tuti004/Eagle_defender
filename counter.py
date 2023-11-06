class Counter:
    def __init__(self):
        self.num = 1

    def increment(self):
        self.num += 1
        if self.num > 3:
            self.num = 1