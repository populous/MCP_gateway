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

### CMake/CTest 테스트 팩

CMake가 테스트 전용 가상환경 생성, `requirements.txt` 설치, 테스트 등록과 실행을 담당합니다.

```powershell
cmake -S . -B build
ctest --test-dir build -C Debug --output-on-failure
```

동일한 테스트 팩을 CMake 타깃으로 실행할 수도 있습니다.

```powershell
cmake --build build --config Debug --target test-pack
```

`dashboard.unit` CTest는 기존 Flask 테스트 클라이언트를 사용해 임시 SQLite 데이터베이스에서 목록 화면 조회와 게시물 등록·영속 저장을 검증합니다. 등록된 테스트 확인 및 라벨 실행 예시는 다음과 같습니다.

```powershell
ctest --test-dir build -C Debug --show-only
ctest --test-dir build -C Debug -L dashboard --output-on-failure
```

이미 의존성이 설치된 Python을 그대로 사용하려면 configure 시 `-DMCP_GATEWAY_SETUP_TEST_ENV=OFF`를 지정할 수 있습니다. 기본값은 격리 환경을 만드는 `ON`입니다.

### 개발용 주의사항

- `flask run --debug`와 `app.py`의 개발 서버는 로컬 개발 전용이며 운영 환경에 그대로 노출하지 마세요.
- 운영 환경에서는 `SECRET_KEY` 환경 변수를 충분히 긴 임의 값으로 설정하세요.
- SQLite 파일은 `instance/` 아래에 생성되고 Git에서 제외됩니다. 중요한 데이터는 별도로 백업하세요.
- CMake 테스트 환경과 생성물은 `build/` 아래에 격리되고 Git에서 제외됩니다. `requirements.txt` 변경 후에는 `cmake -S . -B build`를 다시 실행하세요.
- 기본 CMake configure는 테스트 의존성을 설치하므로 패키지 인덱스에 접근할 수 있어야 합니다. 오프라인 환경에서는 의존성을 미리 설치하고 `-DMCP_GATEWAY_SETUP_TEST_ENV=OFF`를 사용하세요.
- 현재는 최소 기능을 위해 자동 테이블 생성만 사용합니다. 스키마가 커지면 Flask-Migrate 같은 마이그레이션 도구를 도입하세요.
- 제목은 120자로 제한되며 제목과 내용은 필수입니다. 추가 공개 기능을 붙일 때는 인증, 권한, CSRF 보호를 함께 검토하세요.
