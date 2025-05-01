from typing import Optional
from pydantic import BaseModel


class MastersGymer(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: str
    gymer_id: int
    
    