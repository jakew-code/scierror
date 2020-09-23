import math

class Measurement:
    """A class to represent a measurement and the associated 
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
        return math.sqrt(error1**2 + error2**2)

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
        new_error = new_value * math.sqrt((self._error/self._value)**2 + 
                                     (other.get_error()/other.get_value())**2)
        return Measurement(new_value, new_error)

    def __truediv__(self, other):
        """Defines division of values and errors."""
        new_value = self._value / other.get_value()
        new_error = new_value * math.sqrt((self._error/self._value)**2 + 
                                     (other.get_error()/other.get_value())**2)
        return Measurement(new_value, new_error)

    @staticmethod
    def sin(measurement):
        """Defines application of the sine function."""
        new_value = math.sin(measurement.get_value())
        new_error = math.fabs(math.cos(measurement.get_value())) \
                    * measurement.get_error()
        return Measurement(new_value, new_error)
    
    @staticmethod
    def cos(measurement):
        """Defines application of the cosine function."""
        new_value = math.cos(measurement.get_value())
        new_error = math.fabs(math.sin(measurement.get_value())) \
                    * measurement.get_error()
        return Measurement(new_value, new_error)

    @staticmethod
    def tan(measurement):
        """Defines the application of the tangent function."""
        new_value = math.tan(measurement.get_value())
        new_error = 1/(math.cos(measurement.get_value()) ** 2) \
                    * measurement.get_error()
        return Measurement(new_value, new_error)

    @staticmethod
    def pow(measurement, power):
        """Defines taking the power of measurements."""
        new_value = math.pow(measurement.get_value(), power)
        new_error = new_value * power * measurement.get_error()/ \
                    measurement.get_value()
        return Measurement(new_value, new_error)
    
    @staticmethod
    def log(measurement):
        """Defines taking log base e."""
        new_value = math.log(measurement.get_value())
        new_error = measurement.get_error()/measurement.get_value()
        return Measurement(new_value, new_error)

    @staticmethod
    def exp(measurement):
        """Defines e^measurement."""
        new_value = math.exp(measurement.get_value())
        new_error = new_value * measurement.get_error()
        return Measurement(new_value, new_error)

    def __str__(self):
        """Returns the string representation of the measurement."""
        return "{} +- {}".format(round(self._value, 4), round(self._error, 4))