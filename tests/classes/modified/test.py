class MathTest(object):
    def __init__(self):
        self.owner = "Kelvin"

    def check_owner(self):
        print("owner: " + self.owner)

    def plus(self, n: int = 3):
        return n + 1

    def plusf(self, f1: float = 0.5, f2: float = 0.5) -> float:
        return f1 + f2

    def minus(self, n: int):
        return n - 1

    def minusf(self, f: float = 0.5):
        return f

    def square(self, n: int = 10):
        return n**2
