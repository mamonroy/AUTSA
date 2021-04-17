class MathTest:
    def __init__(self):
        self.owner = "Miffy"

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

    def power(self, n: int = 2):
        power = self.plus(5)
        return n**power
    
    def giveOne(self):
        return 1
