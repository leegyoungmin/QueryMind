from typing import Dict, Any, Optional
from src.adapters.postgresql_adapter import PostgreSQLAdapter
from src.adapters.mysql_adapter import MySQLAdapter

class DBManager:
    def __init__(self):
        self.adapters = {
            'postgresql': PostgreSQLAdapter,
            'mysql': MySQLAdapter
        }
        self.connections = {}

    def connect_to_database(self, db_type: str, connection_string: str) -> str:
        if db_type not in self.adapters:
            raise ValueError(f"지원하지 않는 데이터베이스 타입입니다: {db_type}")

        adapter_class = self.adapters[db_type]
        adapter = adapter_class()
        connection_id = adapter.connect(connection_string)

        self.connections[connection_id] = adapter
        return connection_id

    def get_schema(self, connection_id: str) -> Dict[str, Any]:
        if connection_id not in self.connections:
            raise ValueError(f"유효하지 않은 연결 ID입니다: {connection_id}")
        
        adapter = self.connections[connection_id]
        return adapter.get_schema()

    def execute_query(self, connection_id: str, query: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if connection_id not in self.connections:
            raise ValueError(f"유효하지 않은 연결 ID입니다: {connection_id}")
        
        adapter = self.connections[connection_id]
        return adapter.execute_query(query, parameters)

    def close_connection(self, connection_id: str) -> Dict[str, str]:
        """데이터베이스 연결을 종료합니다."""
        if connection_id not in self.connections:
            raise ValueError(f"유효하지 않은 연결 ID입니다: {connection_id}")
            
        adapter = self.connections[connection_id]
        adapter.close()
        del self.connections[connection_id]
        
        return {"message": "연결이 성공적으로 종료되었습니다."}