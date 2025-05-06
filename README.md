# db-connector-helper-mcp MCP 서버 문서
db-connector-helper-mcp는 MCP 서버 기반의 데이터베이스 쿼리 도우미 애플리케이션입니다. 이 문서는 프로젝트의 주요 기능, 설치 방법, 사용 방법 등을 상세히 설명합니다.

## 프로젝트 소개
db-connector-helper-mcp는 MCP 서버 기반의 데이터베이스 쿼리 도우미 도구입니다. 
AI를 통하여 데이터베이스에 자연어를 활용한 질의가 가능합니다.


## 기술 스택
- Python
- FastMCP
- PostgreSQL/MySQL

## 서버 설정
db-connector-helper-mcp를 MCP Claude Desktop Application에 연결하기 위해서는 다음 설정이 필요합니다:

0. `git clone https://github.com/leegyoungmin/db-connector-helper.git`를 실행하여 프로젝트를 clone합니다.

1. `claude_desktop_config.json` 파일을 수정합니다:

```json
{
    "mcpServers": {
        "db-connector-helper": {
            "command": "uv",
            "args": [
                "run",
                "--directory={user project cloned path}/server",
                "server.py",
                "--transport=stdio"
            ]
        }
    }
}
```

2. MCP Claude Desktop Application을 실행합니다.

## 지원

문제나 제안사항이 있다면 GitHub 이슈를 통해 알려주세요.
