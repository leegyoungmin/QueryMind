from typing import Dict, Any
from mcp.server import FastMCP

from src.models.database import DatabaseSchema

class SQLGenerator:
    def __init__(self, mcp: FastMCP):
        self.mcp = mcp

    def natural_language_to_sql(self, query: str, schema: DatabaseSchema, db_type: str = "postgresql") -> str:
        schema_text = self._format_schema(schema)
        
        prompt = self.mcp.sql_generation_prompt(
            schema_text=schema_text,
            query=query,
            db_type=db_type
        )

        response = self.mcp.generate(
            prompt=prompt,
            system_prompt="""
            데이터베이스 전문가로서 자연어를 SQL로 변환합니다. SQL 쿼리만 반환하고 다른 설명은 하지 마세요.
            또한 쿼리 실행 결과를 반환하지 말고, 텍스트로 반환해주세요.
            그 어떤 결과도 반환하지 말고, 오직 쿼리만 반환해주세요.
            """,
            temperature=0,
            max_tokens=1000
        )

        return response.strip()

    def _format_schema(self, schema: DatabaseSchema) -> str:
        text_parts = []

        for table_name, table_info in schema.tables.items():
            text_parts.append(f"테이블: {table_name}")
            text_parts.append("컬럼:")

            for column_name, column_info in table_info.columns.items():
                pk_marker = " (PK)" if column_name in table_info.primary_keys else ""
                is_nullable = "" if column_info.nullable else " NOT NULL"

                text_parts.append(f"  - {column_name}: {column_info.type}{pk_marker}{is_nullable}")

            text_parts.append("")

        return "\n".join(text_parts) 