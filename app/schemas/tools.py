from pydantic import BaseModel
from typing import Any

class Tools(BaseModel):
    tool_name: str
    args: dict[str, Any]