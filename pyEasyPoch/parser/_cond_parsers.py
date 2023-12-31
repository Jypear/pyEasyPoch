import re
from pyEasyPoch.exceptions import pyEasyPochParsingException
from ._parser_types import (
    StyleEnum,
    OffsetEnum,
    TimeExpressionsEnum
)

def condition_parser(arg: str):

    return {
        "time": _parse_timestamp(arg),
        "offset": _parse_offset(arg),
        "recursive": _parse_recursion(arg),
        "until": _parse_end(arg)
    }

def _find_matching_time_expressions(arg: str):
    all_time_items = re.findall(r"(\d{1,11})\s?(seconds|second|minutes|minute|hours|hour|days|day)", arg)
    return all_time_items

def _split_until_statement(arg: str, split:str = "pre"):
    split_options = ["pre", "post"]
    if split not in split_options:
        raise pyEasyPochParsingException(
            "When splitting until statement, undefined split option was passed into function."
        )
    r = re.search(r"(.*)until(.*)", arg, re.IGNORECASE)
    data = arg
    if r:
        if split == "pre":
            data = r.group(1).strip()
        elif split == "post":
            data = r.group(2).strip()
    return data

def _parse_timestamp(arg: str):
    _time_arg = {}
    arg = _split_until_statement(arg)
    r = re.search(r"(now)|(epoch) (\d{1,64})|(time) ([\d,\-,\:,\/,\ ]{1,64})", arg, re.IGNORECASE)
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
    _time_arg = {}
    r = re.search(r"(((\d{1,11})\s?(seconds|second|minutes|minute|hours|hour|days|day)\s?)*)(after|before)", arg, re.IGNORECASE)
    if r:
        offset = {
            "seconds": 0,
            "minutes": 0,
            "hours": 0,
            "days": 0
        }
        time_expression_map = {
            TimeExpressionsEnum.DAY: "days",
            TimeExpressionsEnum.DAYS: "days",
            TimeExpressionsEnum.HOUR: "hours",
            TimeExpressionsEnum.HOURS: "hous",
            TimeExpressionsEnum.MINUTE: "minutes",
            TimeExpressionsEnum.MINUTES: "minutes",
            TimeExpressionsEnum.SECOND: "seconds",
            TimeExpressionsEnum.SECONDS: "seconds"
        }
        try:
            _time_arg["style"] = OffsetEnum(r.group(5).lower())
        except Exception as err:
            raise pyEasyPochParsingException("Error capturing after or before offset argument") from err
        matched_expressions = _find_matching_time_expressions(r.group(1).lower())
        if len(matched_expressions) == 0:
            raise pyEasyPochParsingException(
                "Detected offset but unable to find matching time expressions"
            )
        else:
            for result in matched_expressions:
                try:
                    time_expression = TimeExpressionsEnum(TimeExpressionsEnum(result[1]))
                except Exception as err:
                    raise pyEasyPochParsingException("Error capturing time expression argument when determining offset") from err
                if time_expression in time_expression_map.keys():
                    offset[time_expression_map[time_expression]] = int(result[0])
        _time_arg["offset"] = offset


    return _time_arg

def _parse_recursion(arg: str):
    _time_arg = False
    r = re.search(r"^(every)\s?\d", arg, re.IGNORECASE)
    if r:
        if "every" in r.group(1).lower():
            _time_arg = True
    return _time_arg

def _parse_end(arg: str):
    _time_arg = {}
    r = re.search(r"until", arg, re.IGNORECASE)
    if r:
        post_statement = _split_until_statement(arg, split="post")
        _time_arg = _parse_timestamp(post_statement)
    return _time_arg