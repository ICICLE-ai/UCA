from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Rule:
    Rule_UUID: str
    CI: str
    Type: str
    Services: List[str]
    Data_Rules: List[dict]
    Active_From: str
    Active_To: Optional[str]
    TapisToken: str
    TAPIS_UUID: str
    Tapis_UserName: str

# TODO: Yet to narrow down final structure 