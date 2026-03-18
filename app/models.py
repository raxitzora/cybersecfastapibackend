from pydantic import BaseModel
from typing import List,Dict,Optional


class ChatRequest(BaseModel):
    user_id:str
    message:str

class ChatResponse(BaseModel):
    reply:str
    model_used:str = "unknown"



