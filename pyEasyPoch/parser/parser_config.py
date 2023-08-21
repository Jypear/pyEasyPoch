from pydantic import BaseModel


class ParserConfig(BaseModel):
    time_arg: str = "now"
    offset_arg: str = ""

    recursive_arg: str = ""
    end_arg: str = ""

    