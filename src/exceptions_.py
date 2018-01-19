class BenzlimException(Exception):
    def __init__(self, message, *args):
        super(BenzlimException, self).__init__(self, message, *args)
        #pyhon 3 hook
        if hasattr(self, "message"):
            self.message = self.message or "%s" % args # str(self.args[2])

    def __str__(self):
        return str(self.__class__.__name__) + ": " + self.message

class StationNotFoundException(BenzlimException):
    def __init__(self, message, *args):
        super(StationNotFoundException, self).__init__(self, message, *args)

class PriceNotFoundException(BenzlimException):
    def __init__(self, message, *args):
        super(PriceNotFoundException, self).__init__(self, message, *args)

class TrainingDataMissingException(BenzlimException):
    def __init__(self, message, *args):
        super(TrainingDataMissingException, self).__init__(self, message, *args)

class BadFormatException(BenzlimException):
    def __init__(self, message, *args):
        super(BadFormatException, self).__init__(self, message, *args)

class BadValueException(BenzlimException):
    def __init__(self, message, *args):
        super(BadValueException, self).__init__(self, message, *args)