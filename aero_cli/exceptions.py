"""
exceptions.py

Custom exception classes.
"""


class APIKeyError(Exception):
    """
    FlightAware AeroAPI key cannot be found on the User's system.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
