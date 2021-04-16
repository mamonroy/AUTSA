def shouldBeIgnored():
    print("Should Not Print This")

def independent(n : int) -> int:
    return n * 2

def dependent(n : int):
    checkFirst = independent(5)
    return checkFirst * 3