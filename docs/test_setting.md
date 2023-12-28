# How to start

github repo fork
```sh
git clone [fork한 본인 repo의 url]
git remote add upstream https://github.com/PNU-AID/AID_Backend_v2.git
# git remote -v
```

## Setting
- [install pyenv](https://github.com/pyenv/pyenv)
  - 윈도우는 이 링크로 설치 : [pyenv-win](https://github.com/pyenv-win/pyenv-win)
- [install poetry](https://python-poetry.org/docs/)
- use Python 3.10.*

## 가상환경 설정 방법
```sh
pyenv install 3.10.11
pyenv local 3.10.11
# 터미널 재시작 혹은 아래 명령어 실행
pyenv shell 3.10.11
poetry config virtualenvs.in-project true
poetry config virtualenvs.path "./.venv"
poetry config --list # poetry config 확인

# poetry lock --no-update
poetry install --no-root
poetry shell
pre-commit install
```
---

## 로컬환경에서 백엔드 서버 여는 방법

[도커 설치](https://www.docker.com/products/docker-desktop/)

일반 local 환경
```py
cd aid_web
python manage.py makemigrations
python manage.py migrate

```
