from math import sqrt

class Measurement:
    """A class to represent an measurement and the associated 
    error."""
    def __init__(self, value, error):
        """Initialises the object with the error and the value."""
        self._value = value
        self._error = error
    
    def get_value(self):
        """Returns the value of the measurement."""
        return self._value

    def get_error(self):
        """Returns the error of the measurement."""
        return self._error

    @staticmethod
    def add_error(error1, error2):
        """Returns the error from adding or subtracting two
        quantities."""
        return sqrt(error1**2 + error2**2)

    def __add__(self, other):
        """Defines addition of values and errors."""
        new_value = self._value + other.get_value()
        new_error = self.add_error(self._error, other.get_error())
        return Measurement(new_value, new_error)

    def __sub__(self, other):
        """Defines subtraction of values and errors."""
        new_value = self._value - other.get_value()
        new_error = self.add_error(self._error, other.get_error())
        return Measurement(new_value, new_error)

    def __mul__(self, other):
        """Defines multiplictaion of values and errors."""
        new_value = self._value * other.get_value()
        new_error = new_value * sqrt((self._error/self._value)**2 + 
                                     (other.get_error()/other.get_value())**2)
        return Measurement(new_value, new_error)

    def __truediv__(self, other):
        """Defines division of values and errors."""
        new_value = self._value / other.get_value()
        new_error = new_value * sqrt((self._error/self._value)**2 + 
                                     (other.get_error()/other.get_value())**2)
        return Measurement(new_value, new_error)

    def __str__(self):
        """Returns the string representation of the measurement."""
        return "{} +- {}".format(round(self._value, 4), round(self._error, 4))