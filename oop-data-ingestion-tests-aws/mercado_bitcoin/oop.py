import datetime
import math


class Person:
    def __init__(self, name: str, last_name: str, birth_date: datetime.date):
        self.birth_date = birth_date
        self.last_name = last_name
        self.name = name

    """
    @property -> a decorator
    """

    @property
    def age(self) -> int:
        return math.floor((datetime.date.today() - self.birth_date).days / 365.2425)

    """
    Overriding the str method to not print <__main__.Person object at 0x000002A936703FD0> anymore
    """

    def __str__(self) -> str:
        return f"{self.name} {self.last_name} is {self.age} years old"


will = Person(name="will", last_name="barbosa", birth_date=datetime.date(1996, 2, 19))

print(will)
print(will.birth_date)
# print(will.how_old_is_you())
print(will.age)
