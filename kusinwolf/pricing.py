import math

# This helps me to display boundless prices in the effert to read EVE market work

class Pricing(object):
    def __init__(self, value):
        modules_value = 1
        temp_value = 0
        self.split_values = []

        self.split_values.append( ("%.2f" % (value % modules_value)).replace('0.', '.') )

        while ( (value - (value % modules_value)) > 0 ):
            temp_value = ( value - (value % modules_value))
            modules_value *= 1000
            temp_value = "%03d" % math.floor( (value % modules_value) / (modules_value / 1000) )
            self.split_values.append( temp_value ) # This is what is left over after removing the last found value set

        self.split_values.reverse() # Reverse the order to get the proper set

    def __repr__(self):
        return ",".join(self.split_values[0:len(self.split_values) - 1]) + self.split_values[-1]
