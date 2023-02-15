import math


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def quadratic_formula(a, b, c):
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return None
    else:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return (x1, x2)


class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)


if __name__ == "__main__":
    print(factorial(5))
    print(quadratic_formula(1, -5, 6))
    rectangle = Rectangle(3, 4)
    print(rectangle.area())
    print(rectangle.perimeter())
