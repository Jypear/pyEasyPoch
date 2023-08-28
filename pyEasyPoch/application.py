import time
import datetime
from pydantic import BaseModel, Field
from typing import Optional
from pyEasyPoch.parser import condition_parser
from pyEasyPoch.exceptions import (
    pyEasyPochFormatException,
    PyEasyPochException
    )


class EasyPoch(BaseModel):
    arg:str = Field(
        default = "now",
        description = "String representation of how the model should behave",
        examples = [
            "now"
            "every 5 minutes after now",
            "every 5 minutes after 1234567",
            "10 seconds after now",
            "5 seconds before now"
        ],
        validate_default = True
    )
    realtime: bool = False
    _time: Optional[int] = None

    # TODO: Need to add validation to make sure that arg follows a correct format
    # TODO: On post init initiate class based on what arg says
    # TODO: Finish dunder methods to allow for comparison and stuff



    def model_post_init(self, _data):
        parsed_argument = condition_parser(self.arg)
        # Logic:
        # with parsed arguments first need to determine what to set the time now
        # check to see if time is defined, if it isn't then just set it to now
        # if recursive keep time as the time defined
        # if not recursive and offset is set then apply the offset to the time
        # if recursive is set then make it iterable
        # use the offset for the recursion else error
        # Set the until time
        self.time = time.time()

    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self, value):
        if self._time:
            raise PyEasyPochException(
                "EasyPoch object does not allow the setting of the time attribute more than once"
            )
        self._time = value

    def __str__(self):
        return str(self.time)
    
    def __int__(self):
        return int(self.time)
    
    def timestamp(self, format:str = None):
        if format:
            if isinstance(format, str):
                try:
                    return str(datetime.datetime.fromtimestamp(self.time).strftime(format))
                except Exception as err:
                    raise pyEasyPochFormatException(
                        "Error when passing timestamp formating into EasyPoch Object. Issue with parsing formating"
                    ) from err
            else:
                raise TypeError(
                    "Timestramp formatting must be a string object"
                )
        return str(datetime.datetime.fromtimestamp(self.time))



    

