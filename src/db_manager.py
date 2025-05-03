import uuid

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text

from typing import Dict, Any, Optional

class DBManager:
    def __init__(self):
        self.connections = {}

    def connect_to_database(self, connection_string: str, credentials: Optional[Dict[str, str]] = None) -> str:
        connection_id = str(uuid.uuid4())

        engine = create_engine(connection_string)
        connection = engine.connect()

        self.connections[connection_id] = {
            'engine': engine,
            'connection': connection,
        }

        return connection_id
    
    def execute_query(self, connection_id: str, query: str) -> Dict[str, Any]:
        if connection_id not in self.connections:
            raise ValueError(f"유효하지 않은 연결 ID입니다. {connection_id}")
        
        connection = self.connections[connection_id]['connection']
        result = connection.execute(text(query))
        
        if query.strip().upper().startswith("SELECT") is False:
            raise ValueError("SELECT 쿼리만 지원합니다.")
        
        rows = []
        for row in result.fetchall():
            row_dict = {}
            for key, value in row._mapping.items():
                row_dict[key] = value
            rows.append(row_dict)

        return rows