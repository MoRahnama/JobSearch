import unittest
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * (self.radius ** 2)

circle = Circle(5)

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "I am an animal." 

class Dog(Animal):
    def speak(self):
        return "Woof!"

dog = Dog("Buddy")
print(dog.speak())  # Output: "Woof!"