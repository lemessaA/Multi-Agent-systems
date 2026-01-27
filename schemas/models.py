from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class AgentType(str, Enum):
    WEATHER = "weather"
    NEWS = "news"
    FINANCE = "finance"
    ROUTER = "router"

class AgentRequest(BaseModel):
    query: str
    agent_type: Optional[AgentType] = None
    location: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    agent_type: AgentType
    response: str
    data: Optional[Dict[str, Any]] = None
    source: str
    confidence: float = 1.0

class MultiAgentResponse(BaseModel):
    responses: List[AgentResponse]
    execution_time: float
    conversation_id: str