from pydantic import BaseModel
from typing import List,Dict


class ChatRequest(BaseModel):
    message:str
    history:List[Dict] = []

class ChatResponse(BaseModel):
    reply:str
    model_used:str = "unknown"



