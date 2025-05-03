import os
import anthropic

from typing import Dict, Any, Optional
from openai import OpenAI

class SQLGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API 키가 필요합니다")
        
        self.client = anthropic.Anthropic(api_key = self.api_key)

    def natural_language_to_sql(self, query: str, schema: Dict[str, Any], db_type: str = "postgresql") -> str:
        schema_text = self._format_schema(schema)

        prompt = f"""
        다음 데이터베이스 스키마를 기반으로 자연어 질의를 SQL 쿼리로 변환해주세요:
        
        {schema_text}
        
        자연어 질의: {query}
        
        데이터베이스 유형: {db_type}
        
        SQL 쿼리:
        """

        response = self.client.messages.create(
            model = "claude-3-5-sonnet-20241022",
            max_tokens = 1000,
            temperature = 0,
            system = """
            데이터베이스 전문가로서 자연어를 SQL로 변환합니다. SQL 쿼리만 반환하고 다른 설명은 하지 마세요.
            또한 쿼리 실행 결과를 반환하지 말고, 텍스트로 반환해주세요.
            그 어떤 결과도 반환하지 말고, 오직 쿼리만 반환해주세요.
            """,
            messages = [
                {"role": "user", "content": prompt}
            ]
        )

        sql_query = response.content[0].text.strip()

        return sql_query

    def _format_schema(self, schema: Dict[str, Any]) -> str:
        text_parts = []

        for table_name, table_info in schema.get('tables', {}).items():
            text_parts.append(f"테이블: {table_name}")
            text_parts.append("컬럼:")

            for column_name, column_info in table_info['columns'].items():
                pk_marker = " (PK)" if column_name in table_info.get("primary_keys", []) else ""
                is_nullable = "" if column_info.get("nullable") else " NOT NULL"

                text_parts.append(f"  - {column_name}: {column_info.get('type')}{pk_marker}{is_nullable}")

            text_parts.append("")

        return "\n".join(text_parts)