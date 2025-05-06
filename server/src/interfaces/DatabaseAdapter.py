from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class DatabaseAdapter(ABC):
    @abstractmethod
    def connect(self, connection_string: str) -> str:
        """데이터베이스에 연결합니다."""
        pass

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """데이터베이스 스키마를 가져옵니다."""
        pass

    @abstractmethod
    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """SQL 쿼리를 실행합니다."""
        pass

    @abstractmethod
    def close(self) -> None:
        """데이터베이스 연결을 종료합니다."""
        pass
