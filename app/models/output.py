from pydantic import BaseModel
from typing import List


class Action(BaseModel):
    tool: str
    name: str
    params: List[str]
    order: int


class OutputModel(BaseModel):
    actions: List[Action]
