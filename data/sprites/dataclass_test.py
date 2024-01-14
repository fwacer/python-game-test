from dataclasses import dataclass

@dataclass(kw_only=True)
class Base():
    a: int = 1
    b: int = 2
    def test_base():
        pass

@dataclass(kw_only=True)
class Child(Base):
    a:int = 4
    b = 5
    c: int = 3
    def test():
        pass


print(Child())