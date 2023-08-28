from pydantic import BaseModel


class ParserConfig(BaseModel):
    time: str = "now"
    offset: str = ""

    recursive: str = ""
    until: str = ""
