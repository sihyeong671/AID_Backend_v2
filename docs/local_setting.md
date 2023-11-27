# How to start

github repo fork
```sh
git clone [fork한 본인 repo의 url]
git remote add upstream ''
git remote -v
# upstream(협업 repo내용)과 동기화 하려면 아래 명령어 실행
git pull upstream dev
# 이후 기능 브랜치 생성하여 작업
git checkout -b feat/<기능 내용>
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
poetry install
poetry shell
pre-commit install
```
---

## 백엔드 서버 여는 방법

[도커 설치](https://www.docker.com/products/docker-desktop/)
