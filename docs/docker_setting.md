# Develop Server

## docker-compose.yaml
- docker compose를 사용해, nginx 서버(미구현), Django, PostgreSQL 서버 각각의 container를 deploy할 수 있도록 해주는 파일
- docker container는 `aid` 이름의 network 사용
- `server` : Django server
  - Django는 `manage.py`를 실행시켜 동작, runserver 이전 makemigrations 및 migrate 수행.
  - 8000번 port 사용
  - Django 내의 `settings.py` 에서 PostgreSQL 서버에 접속하기 위한 환경 변수 파일은 `./env/.server.env` 사용
- `db` : PostgreSQL server
  - `postgres:16-alpine` image 사용. 효율성을 위해 가벼운 alpine linux 사용
  - database 파일은 `/var/lib/postgresql/data` mount
  - PostgreSQL container는 5432 port를 통해 접속 가능하도록 설정
  - 환경 변수 파일은 `./env/.db.env`사용
- PostgreSQL environment variable
  - `POSTGRES_USER` : PostgreSQL에 접속할 사용자(지정하지 않으면 `postgres`사용.)
  - `POSTGRES_PASSWORD` : PostgreSQL 비밀번호
  - `POSTGRES_DB` : 생성할 데이터베이스 이름
  - `TZ` : timezone. `TZ=Asia/Seoul`로 지정.
  ```
  # .db.env

  POSTGRES_USER=****
  POSTGRES_PASSWORD=****
  POSTGRES_DB=****
  TZ=Asia/Seoul
  ```

## Dockerfile
Django용 이미지 생성을 위한 Dockerfile. poetry 설치 후, pyproject.toml 내의 패키지 설치
Django 서버 이미지 생성을 위한 도커 파일
