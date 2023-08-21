import re
from enum import Enum
from pyEasyPoch.parser.parser_config import ParserConfig

class StyleEnum(Enum):
    EPOCH = "epoch"
    TIMESTAMP = "timestamp"
    STRING = "string"


def condition_parser(arg: str):
    # Determine in string the time that needs to be set
        # This is going to either be 'now' or an actual date/time or epoch
        # examples now, from now, before now, 1234567, 12:34 11/12/2023
    # After that need to determine if an argument of time is used before 'before' or 'after'
        # 5 minutes before, 10 seconds after
    # Then need to determine if the string starts with "every" if it does it needs to be recursive
    # Then need to determine if until is used if it is the recursion has a set ending time
    _time_arg = _parse_timestamp(arg)


def _parse_timestamp(arg: str):

    _time_arg = {}
    r = re.search(r"(now)|(epoch) (\d{1,64})|(time) ([\d,\-,\:,\/,\ ]{1,64})", arg)
    if r:
        if r.group(1):
            _time_arg = {
                "arg": r.group(1),
                "style": StyleEnum.STRING
            }
        elif r.group(2):
            _time_arg = {
                "arg": r.group(3),
                "style": StyleEnum.EPOCH
            }
        elif r.group(4):
            _time_arg = {
                "arg": r.group(5),
                "style": StyleEnum.TIMESTAMP
            }

    
    return _time_arg


def _parse_offset(arg: str):
    pass

def _parse_recursion(arg: str):
    pass

def _parse_end(arg: str):
    pass