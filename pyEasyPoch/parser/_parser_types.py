from enum import Enum

class StyleEnum(Enum):
    EPOCH = "epoch"
    TIMESTAMP = "timestamp"
    STRING = "string"

class OffsetEnum(Enum):
    BEFORE = "before"
    AFTER = "after"

class TimeExpressionsEnum(Enum):
    SECOND = "second"
    SECONDS = "seconds"
    MINUTE = "minute"
    MINUTES = "minutes"
    HOUR = "hour"
    HOURS = "hours"
    DAY = "day"
    DAYS = "days"
