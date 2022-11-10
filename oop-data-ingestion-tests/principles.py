import datetime
import math
from typing import List

""" Principles
- single responsability
- open close (close for modification open for extension)
"""
class Person:
    def __init__(self, name: str, last_name: str, birth_date: datetime.date) -> None:
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

class Resume:
    def __init__(self, person: Person, experiences: List[str]):
        self.person = person
        self.experiences = experiences

    @property
    def number_of_experiences(self) -> int:
        return len(self.experiences)

    @property
    def current_job_title(self) -> str:
        return self.experiences[-1]

    def add_experience(self, experience: str ) -> None:
        self.experiences.append(experience)

    def __str__(self) -> str:
        return f"{self.person.name} {self.person.last_name} is {self.person.age} years old and " \
               f"already worked in {self.number_of_experiences} companies and currently is working on {self.current_job_title}"

will = Person(name='will', last_name='barbosa', birth_date=datetime.date(1996, 2, 19))
resume_will = Resume(person=will, experiences=['FIT', 'GFT', 'AvenueCode'])

#print(resume_will)
#resume_will.add_experience("how education")
#print(resume_will)

class Living:
    def __init__(self, name: str, birth_date: datetime.date) -> None:
        self.name = name
        self.birth_date = birth_date

    @property
    def age(self) -> int:
        return math.floor((datetime.date.today() - self.birth_date).days / 365.2425)

    def make_some_sound(self, noise: str):
        print(f"{self.name} did some noise: {noise}")

# Inheritance -> Open Close principle
class PersonInheritance(Living):
    def __str__(self) -> str:
        return f"{self.name} is {self.age} years old"

    def talking(self, phrase):
        return self.make_some_sound(phrase)

class Dog(Living):
    def __init__(self, name: str, birth_date: datetime.date, race: str):
        super().__init__(name, birth_date) # super -> We're extending from Living Class with name and birth_date
        self.race = race

    def __str__(self) -> str:
        return f"{self.name} is from race {self.race} and is {self.age} years old"

    def late(self):
        return self.make_some_sound('au au!')


didi = PersonInheritance(name='indy', birth_date=datetime.date(1999, 11, 17))
#print(didi)

dog = Dog(name="Simba", birth_date=datetime.date(2018, 4, 15), race='Pastor Belga')
print(dog.late())
print(dog.late())
print(dog.late())
didi.talking("cala a boca simba")
print(dog.late())