class BenzlimException(Exception):
    def __init__(self, *args, **kwargs):
        super(BenzlimException, self).__init__(self, *args, **kwargs)

class StationNotFoundException(BenzlimException):
    def __init__(self, *args, **kwargs):
        super(StationNotFoundException, self).__init__(self, *args, **kwargs)

class PriceNotFoundException(BenzlimException):
    def __init__(self, *args, **kwargs):
        super(PriceNotFoundException, self).__init__(self, *args, **kwargs)

class TrainingDataMissingException(BenzlimException):
    def __init__(self, *args, **kwargs):
        super(TrainingDataMissingException, self).__init__(self, *args, **kwargs)