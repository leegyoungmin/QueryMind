from typing import Dict, Optional, Any

from src.db_manager import DBManager
from src.sql_generator import SQLGenerator
from src.security import SecurityValidator

from mcp.server import FastMCP

from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("query-mind-mcp")

db_manager = DBManager()
sql_generator = SQLGenerator()
security_validator = SecurityValidator()

@mcp.tool()
def connect_database(db_type: str, connection_string: str) -> Dict[str, Any]:
    """
    데이터베이스에 연결합니다.
    
    Args:
        db_type: 데이터베이스 유형 (postgresql, mysql, sqlite 등)
        connection_string: 데이터베이스 연결 문자열
        
    Returns:
        연결 상태 및 ID
    """
    try:
        connection_id = db_manager.connect_to_database(db_type, connection_string)
        return {
            "connection_id": connection_id,
            "status": "connected",
            "message": f"{db_type} 데이터베이스에 성공적으로 연결되었습니다."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@mcp.tool()
def discover_schema(connection_id: str) -> Dict[str, Any]:
    try:
        schema = db_manager.get_schema(connection_id)
        return {
            "status": "success",
            "schema": schema
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"스키마 검색 실패: {str(e)}"
        }

@mcp.tool()
def natural_language_to_sql(connection_id: str, query: str) -> Dict[str, Any]:
    try:
        # 스키마 정보 가져오기
        schema_info = db_manager.get_schema(connection_id)
        
        # 자연어를 SQL로 변환
        sql_query = sql_generator.natural_language_to_sql(query, schema_info)
        
        # SQL 쿼리 보안 검증
        is_valid, error_message = security_validator.validate_query(sql_query)
        if not is_valid:
            return {
                "status": "error",
                "message": error_message
            }
        
        return {
            "status": "success",
            "sql_query": sql_query
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@mcp.tool()
def execute_query(connection_id: str, query: str) -> Dict[str, Any]:
    try:
        # SQL 쿼리 보안 검증
        is_valid, error_message = security_validator.validate_query(query)
        if not is_valid:
            return {
                "status": "error",
                "message": error_message
            }
        
        # 쿼리 실행
        result = db_manager.execute_query(connection_id, query)
        
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
@mcp.tool()
def query_in_natural_language(connection_id: str, query: str) -> Dict[str, Any]:
    try:
        sql_response = natural_language_to_sql(connection_id, query)

        if sql_response["status"] == "error":
            return sql_response
        
        sql_query = sql_response['sql_query']

        result = execute_query(connection_id, sql_query)

        return {
            "status": "success",
            "sql_query": sql_query,
            "result": result["result"]
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@mcp.tool()
def close_connection(connection_id: str) -> Dict[str, Any]:
    """
    데이터베이스 연결을 종료합니다.
    
    Args:
        connection_id: 종료할 연결 ID
        
    Returns:
        결과 메시지
    """
    try:
        result = db_manager.close_connection(connection_id)
        return {
            "status": "success",
            "message": result["message"]
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    mcp.run(transport='sse')