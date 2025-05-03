from typing import Dict, Optional, Any

from src.db_manager import DBManager

from mcp.server import FastMCP

mcp = FastMCP("query-mind-mcp")

db_manager = DBManager()

@mcp.tool()
def hello(name: str) -> str:
    return f"안녕하세요, {name}님! Query Mind 서버에 오신 것을 환영합니다!"


@mcp.tool()
def connect_database(connection_string: str, credentials: Optional[Dict[str, str]] = None) -> str:
    try:
        connection_id = db_manager.connect_to_database(connection_string, credentials)
        return {
            "connectionId": connection_id,
            "status": "connected",
            "message": "데이터베이스에 성공적으로 연결되었습니다."
        }
    except Exception as e:
        return {
            "connectionId": None,
            "status": "error",
            "message": f"데이터베이스 연결 실패: {str(e)}"
        }
    
@mcp.tool()
def execute_query(connection_id: str, query: str) -> Dict[str, Any]:
    try:
        result = db_manager.execute_query(connection_id, query)
        return {
            "status": "success",
            "message": "쿼리가 성공적으로 실행되었습니다.",
            "result": result
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"쿼리 실행 실패: {str(e)}"
        }

if __name__ == "__main__":
    mcp.run(transport = 'stdio')