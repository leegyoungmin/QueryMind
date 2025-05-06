from sqlalchemy import create_engine, text, inspect
from typing import Dict, Any, Optional
from uuid import uuid4
from src.interfaces.DatabaseAdapter import DatabaseAdapter

class PostgreSQLAdapter(DatabaseAdapter):
    def __init__(self):
        self.connection_id = str(uuid4())
        self.engine = None
        self.connection = None
        self.inspector = None

    def connect(self, connection_string: str) -> str:
        try:
            self.engine = create_engine(connection_string)
            self.connection = self.engine.connect()
            self.inspector = inspect(self.engine)
            return self.connection_id
        except Exception as e:
            raise ValueError(f"PostgreSQL 연결 실패: {str(e)}")

    def get_schema(self) -> Dict[str, Any]:
        try:
            schema_info = {"tables": {}}
            
            # PostgreSQL에서 스키마는 기본적으로 'public'으로 처리
            schema_name = 'public'
            
            # 모든 테이블 조회
            for table_name in self.inspector.get_table_names(schema=schema_name):
                columns = {}
                
                # 각 테이블의 컬럼 정보 조회
                for column in self.inspector.get_columns(table_name, schema=schema_name):
                    columns[column['name']] = {
                        'type': str(column['type']),
                        'nullable': column['nullable'],
                        'default': column['default']
                    }
                
                # 기본 키 정보 조회
                primary_keys = self.inspector.get_pk_constraint(table_name, schema=schema_name).get("constrained_columns", [])
                
                schema_info['tables'][table_name] = {
                    'columns': columns,
                    'primary_keys': primary_keys
                }
            
            return schema_info
        except Exception as e:
            raise ValueError(f"스키마 정보 조회 실패: {str(e)}")

    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            result = self.connection.execute(text(query), parameters if parameters else None)
            
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
            self.connection.rollback()
            raise e

    def close(self) -> None:
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()
        self.connection = None
        self.engine = None
        self.inspector = None
