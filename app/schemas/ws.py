from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional, List


class WebSocketMessage(BaseModel):
    type: str
    timestamp: datetime = datetime.now()
    payload: Dict[str, Any] | None
    sender_id: str | None
    target_id: List[str] | []
    command: Optional[str] = None  # 可选字段
