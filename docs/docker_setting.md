# Develop Server

## docker-compose.yaml
- docker compose를 사용해, nginx 서버(미구현), Django, MySQL 서버 각각의 container를 deploy할 수 있도록 해주는 파일
- docker container는 `aid` 이름의 network 사용
- `server` : Django server
  - Django는 `manage.py`를 실행시켜 동작, runserver 이전 makemigrations 및 migrate 수행.
  - db server가 완전히 열린 후 django server가 열려야 하므로 health check를 통해 MySQL 서버가 정상적으로 동작할 때 django container deploy.
  - 8000번 port 사용
  - Django 내의 `settings.py` 에서 MySQL 서버에 접속하기 위한 환경 변수 파일은 `./env/.server.env` 사용
- `db` : MySQL server
  - mysql image 사용
  - database 파일은 `/var/lib/mysql`에 mount
  - MySQL container는 3306 port를 통해 접속 가능하도록 설정
  - 환경 변수 파일은 `./env/.db.env`사용
  - health checking을 위해 MySQL 서버에 ping. 실패 시 5초마다 재시도.
  - DB 내 한글 사용을 위해 유니코드 설정(`mysqld --character-set-server=utf8 --collation-server=utf8_general_c`)
- MySQL environment variable
  - `MYSQL_USER` : MySQL에 접속할 사용자
  - `MYSQL_ROOT_PASSWORD` : MySQL root user 비밀번호(필수로 지정해야 함.)
  - `MYSQL_PASSWORD` : MYSQL_USER에 대한 비밀번호
  - `MYSQL_HOST` : MySQL 서버 host name. container 이름에 맞게 `db`로 설정
  - `MYSQL_DATABASE` : 생성할 데이터베이스 이름
  ```
  # .db.env

  MYSQL_USER=****
  MYSQL_ROOT_PASSWORD=****
  MYSQL_PASSWORD=****
  MYSQL_HOST=db
  MYSQL_DATABASE=****
  ```

## Dockerfile
Django용 이미지 생성을 위한 Dockerfile. poetry 설치 후, pyproject.toml 내의 패키지 설치
Django 서버 이미지 생성을 위한 도커 파일
