from typing import Dict, Any, List
from pydantic import BaseModel

class ColumnInfo(BaseModel):
    type: str
    nullable: bool = True

class TableInfo(BaseModel):
    columns: Dict[str, ColumnInfo]
    primary_keys: List[str] = []

class DatabaseSchema(BaseModel):
    tables: Dict[str, TableInfo] 