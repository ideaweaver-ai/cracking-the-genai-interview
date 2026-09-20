"""Run all examples or one: python 13_class_basics.py methods"""


class Student:
    """A class is a blueprint; each instance stores its own data."""

    school = "Python Academy"  # Class attributes are shared by every student.

    def __init__(self, name, score=0):
        self.name = name
        self.score = score

    def study(self, points):
        self.score += points
        return f"{self.name}'s score is now {self.score}"


def create_objects():
    ada = Student("Ada", 80)
    lin = Student("Lin", 90)
    print(ada.name, lin.score, Student.school)


def methods():
    student = Student("Ada")
    print(student.study(10))  # Instance methods use self to access object data.


def instance_attributes():
    first = Student("Ada")
    second = Student("Lin")
    first.score = 25
    print(first.score, second.score)  # Each object keeps separate instance attributes.


EXAMPLES = {"objects": create_objects, "methods": methods, "attributes": instance_attributes}

if __name__ == "__main__":
    import sys

    for example in ([sys.argv[1]] if len(sys.argv) > 1 else EXAMPLES):
        EXAMPLES[example]()
