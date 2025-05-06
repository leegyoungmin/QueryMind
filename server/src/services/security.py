import re
from typing import Tuple

class SecurityValidator:
    """SQL 쿼리 보안 검증 클래스"""
    
    def __init__(self, read_only=True):
        self.read_only = read_only
        self.forbidden_commands = [
            "DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE", "INSERT", "UPDATE",
            "GRANT", "REVOKE"
        ]
    
    def validate_query(self, query: str) -> Tuple[bool, str]:
        """SQL 쿼리의 안전성을 검증합니다."""
        # 읽기 전용 모드인 경우 SELECT 쿼리만 허용
        if self.read_only and not query.strip().upper().startswith("SELECT"):
            return False, "읽기 전용 모드에서는 SELECT 쿼리만 허용됩니다"
        
        # 금지된 명령어 확인
        for command in self.forbidden_commands:
            pattern = r'\b' + re.escape(command) + r'\b'
            if re.search(pattern, query.upper()):
                return False, f"보안상의 이유로 {command} 명령은 허용되지 않습니다"
        
        return True, ""