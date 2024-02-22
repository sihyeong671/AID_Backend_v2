# Docker

## 환경 별 docker-compose 및 실행 방법
Develop(Local) Server 개발 환경: PostgreSQL database 서버는 docker로 띄우고, Django는 local에서 실행

Test 환경 : PostgreSQL database 서버 및 Django 모두 docker로 실행

## docker관련 파일 구성요소
**docker-compose.yaml**
- docker compose를 사용해, nginx 서버, Django, PostgreSQL 서버 각각의 container를 deploy할 수 있도록 해주는 파일
- docker container는 `aid` 이름의 network 사용
- `server` : Django server
  - test, production 환경에서만 deploy.
  - Django는 `manage.py`를 실행시켜 동작, runserver 이전 makemigrations 및 migrate 수행.
  - 8000번 port 사용
  - Django 내의 `settings.py` 에서 PostgreSQL 서버에 접속하기 위한 환경 변수 파일은 `./env/.server.env` 사용
  - `DJANGO_SETTINGS_MODULE` 환경변수를 이용해 각 배포 환경에 따라 다른 django settings 파일을 사용함.
- `db` : PostgreSQL server
  - `postgres:16-alpine` image 사용. 효율성을 위해 가벼운 alpine linux 사용
  - database 파일은 `/var/lib/postgresql/data` mount
  - PostgreSQL container는 5432 port를 통해 접속 가능하도록 설정
  - 환경 변수 파일은 `./env/.db.env`사용
- `nginx`
  - test, production 환경에서만 사용(이후 https 연결 및 load balancing 등의 기능을 위해)
  - `./config/nginx.test.conf` 및 `nginx.prod.conf`의 nginx conf 파일을 사용
- PostgreSQL environment variable(env에서 확인)
  - `POSTGRES_USER` : PostgreSQL에 접속할 사용자(지정하지 않으면 `postgres`사용.)
  - `POSTGRES_PASSWORD` : PostgreSQL 비밀번호
  - `POSTGRES_DB` : 생성할 데이터베이스 이름
  - `TZ` : timezone. `TZ=Asia/Seoul`로 지정.
- test, production환경에서는 django의 `runserver` 대신, `gunicorn` 사용
  - django 공식문서에서도 배포 환경에서 runserver 사용을 권장하지 않고, gunicorn을 사용하면 요청 분산이 가능해짐.

### Dockerfile
Django용 이미지 생성을 위한 Dockerfile. poetry 설치 후, pyproject.toml 내의 패키지 설치
Django 서버 이미지 생성을 위한 도커 파일
