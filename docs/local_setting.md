# How to start

github repo fork(모든 브랜치 가져오도록 함)
```sh
git clone [fork한 본인 repo의 url]
git remote add upstream https://github.com/PNU-AID/AID_Backend_v2.git
# git remote -v
git checkout dev
```
```sh
# main 브랜치만 가져왔을 경우 아래 명령어 실행
# git checkout -b dev upstream/dev
```

## Setting
- [install pyenv](https://github.com/pyenv/pyenv)
  - 윈도우는 이 링크로 설치 : [pyenv-win](https://github.com/pyenv-win/pyenv-win)
- [install poetry](https://python-poetry.org/docs/)
- use Python 3.10.*

## 가상환경 설정 방법
```sh
pyenv install 3.10.*
pyenv local 3.10.*
# 터미널 재시작 혹은 아래 명령어 실행
pyenv shell 3.10.*
poetry config virtualenvs.in-project true
poetry config virtualenvs.path "./.venv"
poetry config --list # poetry config 확인

# poetry lock --no-update
poetry install --no-root
poetry shell
pre-commit install
```
---
## 환경변수 파일 생성

```sh
# aid_web/.local.env 생성
postgresql_user=admin
postgresql_password=admin1234
postgresql_db_name=test_db
postgresql_host=localhost
postgresql_port=5432

# env/.db.env
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin1234
POSTGRES_DB=test_db
TZ=Asia/Seoul
```

---

## 로컬환경에서 백엔드 서버 여는 방법
[install docker](https://www.docker.com/products/docker-desktop/)
Django는 local, DB는 docker를 통해 띄움

```sh
docker compose -f docker-compose.local.yaml up -d

cd aid_web

# 슈퍼유저 생성
# python manage.py createsuperuser

# 최초실행 혹은 변경사항 있을 경우 아래 명령어 실행
# python manage.py makemigrations
# python manage.py migrate

python manage.py runserver [--settings=config.settings.local]

```
127.0.0.1:8000에서 동작 확인


## DB 내리기

```sh
docker compose -f docker-compose.local.yaml down
# docker compose -f docker-compose.local.yaml down -v
```
