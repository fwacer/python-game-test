from dataclasses import dataclass

class Base():
    def __init__(a: int = 1, b: int)
    a: int
    b: int = 2
    def test_base():
        pass

@dataclass(kw_only=True)
class Child(Base):
    a:int = 4
    c: int = 3
    def test():
        pass


print(Child())