from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

@dataclass
class ToolParameter:
    name: str
    parameter_type: str
    description: str
    required: bool = False
    default: Any = None

@dataclass
class Tool:
    name: str
    description: str
    parameters: List[ToolParameter]
    metadata: Optional[Dict[str, Any]] = None
    identifier: str = ""
    
@dataclass
class ToolInvokeResult:
    content: str
    error_code: int