from typing import Optional
from pydantic import BaseModel

class MoveDetails(BaseModel):
    power: Optional[int]
    pp: Optional[int]
    accuracy: Optional[int]
    type: Optional[str]
    damage_class: Optional[str]