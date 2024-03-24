# How to start


## Fork
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


## Clone
```sh
git clone https://github.com/PNU-AID/AID_Backend_v2.git
# git checkout -b origin/dev
```


## Setting

_서버 개발자거나 필요한 경우에만 설치하면 됩니다_
> - [install pyenv](https://github.com/pyenv/pyenv)
>   - 윈도우는 이 링크로 설치 : [pyenv-win](https://github.com/pyenv-win/pyenv-win)
> - [install poetry](https://python-poetry.org/docs/)
> - use Python 3.10.*

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
postgresql_host=db # docker contatiner 이름으로 정해주어야 인식합니다.
postgresql_port=5432

# env/.db.env
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin1234
POSTGRES_DB=test_db
TZ=Asia/Seoul
```

---

## 로컬 서버 열기
[install docker](https://www.docker.com/products/docker-desktop/)

```sh
# unix 계열이라면 아래 명령어 실행
# sh run_server.sh
docker compose -f docker-compose.local.yaml up -d
```
127.0.0.1:8000에서 동작 확인


## 로컬 서버 닫기

```sh
# unix 계열이라면 아래 명령어 실행
# sh down_server.sh
docker compose -f docker-compose.local.yaml down
# docker compose -f docker-compose.local.yaml down -v
```
