# MCP_gateway

- 로칼에서 사진하나를 카카오를 통해 업로드함.
- 이번에는 Github Oring을 diff를 동기화

## Flask 게시 대시보드

공지와 게시물을 카드 형태로 보여 주고, 같은 화면에서 새 게시물을 등록하는 간단한 Flask 애플리케이션입니다. 게시물은 SQLite의 `instance/dashboard.sqlite3`에 저장됩니다.

### 실행 방법

Windows PowerShell 기준:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
flask --app app run --debug
```

브라우저에서 `http://127.0.0.1:5000`을 엽니다. 첫 실행 시 SQLite 데이터베이스와 테이블이 자동 생성됩니다.

### 테스트

```powershell
python -m unittest discover -s tests -v
```

테스트는 임시 SQLite 데이터베이스를 사용해 목록 화면 조회와 게시물 등록·영속 저장을 검증합니다.

### 개발용 주의사항

- `flask run --debug`와 `app.py`의 개발 서버는 로컬 개발 전용이며 운영 환경에 그대로 노출하지 마세요.
- 운영 환경에서는 `SECRET_KEY` 환경 변수를 충분히 긴 임의 값으로 설정하세요.
- SQLite 파일은 `instance/` 아래에 생성되고 Git에서 제외됩니다. 중요한 데이터는 별도로 백업하세요.
- 현재는 최소 기능을 위해 자동 테이블 생성만 사용합니다. 스키마가 커지면 Flask-Migrate 같은 마이그레이션 도구를 도입하세요.
- 제목은 120자로 제한되며 제목과 내용은 필수입니다. 추가 공개 기능을 붙일 때는 인증, 권한, CSRF 보호를 함께 검토하세요.
