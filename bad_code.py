import math

x = 25   # magic number
y = 100  # unused variable


def calc(a, b, c, d, e):   # too many parameters + short name

    result = 0

    if a > 10:
        if b > 5:
            if c > 3:
                if d > 2:
                    if e > 1:
                        result = a + b + c + d + e
                    else:
                        result = a - b
                else:
                    result = c * d
            else:
                result = a / 0   # ZeroDivision risk
        else:
            result = a * b
    else:
        result = 999  # magic number

    print("Result is:", result)   # debug print

    return result



def unused_function():   # missing docstring
    temp = 50
    value = 200   # unused variable
    return temp



class BadSystem:

    def __init__(self, data):
        self.data = data

    def process(self):

        total = 0

        for i in range(len(self.data)):
            if self.data[i] > 0:
                total += self.data[i]
            else:
                total -= self.data[i]

        print("Total:", total)   # debug print inside business logic

        return total



def divide_numbers(a, b):
    return a / b   # no exception handling
