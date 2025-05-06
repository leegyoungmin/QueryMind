import uuid

from sqlalchemy import create_engine, text, inspect

from typing import Dict, Any, Optional

class DBManager:
    def __init__(self):
        self.connections = {}

    def connect_to_database(self, db_type: str, connection_string: str) -> str:
        connection_id = str(uuid.uuid4())

        try:
            engine = create_engine(connection_string)
            connection = engine.connect()

            self.connections[connection_id] = {
                'engine': engine,
                'connection': connection,
                'type': db_type,
                'inspector': inspect(engine)
            }

            return connection_id
        except Exception as e:
            raise ValueError(f"데이터베이스 연결 실패: {str(e)}")
    
    def get_schema(self, connection_id: str) -> Dict[str, Any]:
        if connection_id not in self.connections:
            raise ValueError(f"유효하지 않은 연결 ID입니다. {connection_id}")
        
        inspector = self.connections[connection_id]["inspector"]
        schema_info = { "tables": {} }

        for table_name in inspector.get_table_names():
            columns = {}

            for column in inspector.get_columns(table_name):
                columns[column['name']] = {
                    'type': str(column['type']),
                    'nullable': column['nullable'],
                    'default': column['default']
                }
            
            primary_keys = inspector.get_pk_constraint(table_name).get("constrained_columns", [])
            schema_info['tables'][table_name] = {
                'columns': columns,
                'primary_keys': primary_keys
            }
        
        return schema_info
    
    def execute_query(self, connection_id: str, query: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if connection_id not in self.connections:
            raise ValueError(f"유효하지 않은 연결 ID입니다. {connection_id}")
        
        connection = self.connections[connection_id]['connection']
        try:
            result = connection.execute(text(query), parameters if parameters else None)
            
            if query.strip().upper().startswith("SELECT") is False:
                raise ValueError("SELECT 쿼리만 지원합니다.")
            
            rows = []
            for row in result.fetchall():
                row_dict = {}
                for key, value in row._mapping.items():
                    row_dict[key] = value
                rows.append(row_dict)

            return rows
        except Exception as e:
            connection.rollback()
            raise e
    
    def close_connection(self, connection_id: str):
        """데이터베이스 연결을 종료합니다."""
        if connection_id not in self.connections:
            raise Exception("유효하지 않은 연결 ID")
            
        connection = self.connections[connection_id]["connection"]
        connection.close()
        
        engine = self.connections[connection_id]["engine"]
        engine.dispose()
        
        del self.connections[connection_id]
        
        return {"message": "연결이 성공적으로 종료되었습니다."}