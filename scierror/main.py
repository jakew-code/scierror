import math
import matplotlib.pyplot as plt
import numpy as np

def latex_table(arrays, here=False):
    """Prints the code for a latex table with empty headings,
    inserting the data provided into rows.
    
    Args:
        arrays: The list of arrays for the table.
        here: True if here tag is to be included.
    """
    # Define a 4-space tab (latex uses 4 space tabs).
    TAB = "    "
    
    cols = len(arrays[0]) + 1

    table_string = (
        "\\begin{table}" + int(here)*"[h]" + "\n" +
        TAB + "\centering\n" + 
        TAB + "\\begin{tabular}{" + cols*'c' + "}\n" +
        2*TAB + "\hline\n" + 
        2*TAB + "" + (cols - 1)*" &" + " \\\\\n" + 
        2*TAB + "\hline\n"
    )

    # Generate each row and add to string.
    for array in arrays:
        new_row = 2*TAB

        for element in array:
            new_row += " & " + str(element)

        new_row += " \\\\\n"
        table_string += new_row

    table_string += (
        2*TAB + "\hline\n" + 
        TAB + "\end{tabular}\n" + 
        TAB + "\caption{}\n" + 
        TAB + "\label{tab:}\n" +
        "\end{table}"
    )

    print(table_string)


class DimensionError(Exception):
    """An error represeting a mismatch of array dimensions."""
    def __init__(self, error_message):
        super().__init__(error_message)


class LinearRegression:
    """A class to perform and plot linear regressions of data with error in 
    the dependent variable."""
    def __init__(self, xdata, ydata, yerr=None):
        self._xdata = xdata
        self._ydata = ydata
        self._yerr = yerr

        self._m = Measurement(0,0)
        self._c = Measurement(0,0)

    def regress(self):
        """Calculates the linear fit and returns the gradient and intercept as 
        measurement objects."""
        n = len(self._xdata)

        # Check that the length of the arrays are the same.
        if len(self._ydata) != n:
            raise DimensionError("dimension mismatch")
        
        if self._yerr is None:
            self._yerr = np.ones(n)*(1/n)
        elif len(self._yerr) != n:
            raise DimensionError("dimension mismatch")

        # Check that all of the arrays are numpy arrays.
        # TODO: Try find a better way to do this.
        if type(self._xdata) is list:
            self._xdata = np.array(self._xdata)
        if type(self._ydata) is list:
            self._ydata = np.array(self._ydata)
        if type(self._yerr) is list:
            self._yerr = np.array(self._yerr)

        # Intermediate calculations.
        wdata = 1/np.power(self._yerr, 2)
        xbar = sum(wdata*self._xdata)/sum(wdata)
        ybar = sum(wdata*self._ydata)/sum(wdata)
        D = sum(wdata*np.power(self._xdata - xbar, 2))

        # Results.
        self._m.set_value(1/D * sum(wdata*(self._xdata - xbar)*self._ydata))
        self._c.set_value(ybar - self._m.get_value()*xbar)
        arrayD = self._ydata - self._m.get_value()*self._xdata \
                    - self._c.get_value()
        self._m.set_error(np.sqrt(1/D * sum(wdata*np.power(arrayD, 2))/(n-2)))
        self._c.set_error(np.sqrt((1/sum(wdata) + np.power(xbar, 2)/D) 
                                    * sum(wdata*np.power(arrayD, 2))/(n-2)))

        return self._m, self._c

    def plot(self, title, xlabel, ylabel, filename=None, show=True, useTex=False, xlim=None, ylim=None):
        """Plots the data points with error bars and the calculated fit.
        
        Args:
            title: Plot title.
            xlabel: x axis title.
            ylabel: y axis title.
            filename: If specified saves plot as filename.
            show: Set to False to hide plots.
            useTex: Set to True to render using tex.
            xlim: Array with x axis bounds.
            ylim: Array with y axis bounds.
        """
        if useTex:
            plt.rcParams.update({
                "text.usetex":True,
                "font.family":"serif"
            })
        
        plt.errorbar(self._xdata, self._ydata, self._yerr, fmt='o', ms=3)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xlim(xlim)
        plt.ylim(ylim)

        # Generate and plot calculated fit.
        Y = self._m.get_value()*self._xdata + self._c.get_value()
        plt.plot(self._xdata, Y)

        if show:
            plt.show()
        
        if filename is not None:
            plt.savefig(filename)


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
        """Returns the absolute error of the measurement."""
        return self._error
    
    def get_relative(self):
        """Returns the relative error of the measurement."""
        return self._error/self._value

    def set_value(self, value):
        """Sets the value of the measurement."""
        self._value = value

    def set_error(self, value):
        """Sets the error of the measurement."""
        self._error = value

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
    def logbase(measurement,b):
        """Defines taking log base b."""
        new_value = math.log(measurement.get_value(),b)
        new_error = measurement.get_error()/ ( math.log(b,math.e) * measurement.get_value() )
        return Measurement(new_value, new_error)

    @staticmethod
    def exp(measurement):
        """Defines e^measurement."""
        new_value = math.exp(measurement.get_value())
        new_error = new_value * measurement.get_error()
        return Measurement(new_value, new_error)

    @staticmethod
    def arcsin(measurement):
        """Defines the application of the arcsine function."""
        new_value = math.asin(measurement.get_value())
        new_error = measurement.get_error() / math.sqrt(1-measurement.get_value() ** 2)
        return Measurement(new_value, new_error)

    @staticmethod
    def arccos(measurement):
        """Defines the application of the arccos function.""" # could also just call arcsin(measurement)
        new_value = math.acos(measurement.get_value())
        new_error = measurement.get_error() / math.sqrt(1-measurement.get_value() ** 2)
        return Measurement(new_value, new_error)

    @staticmethod
    def arctan(measurement):
        """Defines the application of the arcsine function."""
        new_value = math.atan(measurement.get_value())
        new_error = measurement.get_error() / (measurement.get_value() ** 2 + 1)
        return Measurement(new_value, new_error)

    def __repr__(self):
        """Returns the string representation of the measurement."""
        return "{} +- {}".format(round(self._value, 4), round(self._error, 4))


class DataFile:
    """Represents a csv file containing data."""
    def __init__(self, filename):
        """Reads the given csv file into a list of rows containing
        the data.
        """
        self._data = []

        # Turn each line of the file into a list and store it.
        with open(filename) as file:
            for line in file:
                line = line.strip().split(',')
                self._data.append(line)

    def read_cols(self, start_row, start_col, end_row, end_col):
        """Takes the designated subsection of the data and returns
        each of the columns as a list with each element converted
        to a float.
        
        Subsection starts at (0,0) and is not inclusive of end 
        row/col.
        """
        if start_row > end_row or start_col > end_col:
            raise IndexError("End row/col coordinate before start coordinate")
        
        arrays = []

        for column in range(start_col, end_col):
            new_array = []

            for row in range(start_row, end_row):
                new_array.append(float(self._data[row][column]))
            
            arrays.append(new_array)
        
        return arrays