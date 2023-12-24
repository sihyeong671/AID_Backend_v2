# Dummy data 생성 setting

### 1. **가상환경 설정 확인**
```bash
poetry shell
```

### 1-1. migration 설정

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. django-seed 설치
```bash
pip install django-seed
```
### 3. `setting.py`에 `django_seed`추가
```python
INSTALLED_APPS = (
    ...
    'django_seed',
)
```

### 4.등록되었는지 확인

```bash
# python manage.py --help 로 잘 등록되었는지 확인
...
[django_seed]
    seed
...
```

### 5. 'psycopg2' 모듈 설치
```bash
pip install psycopg2
```

### 6(Final). 사용하기

- APPNAME 앱에 15개의 dummy data 생성

```bash
python manage.py seed testapp --number=15
```

다만, field의 type을 기준으로 dummy data를 작성하므로
**세부적인 조절 못함.**

ex) user의 email에는 emailType으로 올바른 예시가 들어가지만, 전화번호는 charType이므로 무작위 문자열이 들어감.

---

# 해결: dummy data의 세부 설정 조절

### 1. app-management-commands `__init__.py` 및 `seed_users.py` 추가

아래 명령어를 순서대로 치면 됨

```bash
# app 폴더로 디렉토리 변경
cd app_name
# 폴더 추가 *이름 고정*
mkdir management
cd management
# 필수 !!
touch __init__.py
# 폴더 추가 *이름 고정*
mkdir commands
cd commands
# 필수 !!
touch __init__.py
# seed를 만들 파일 추가
touch seed_users.py
```

##### 성공적인 경우의 폴더 구조
`__pycahche__` 는 무시해도 됨
```bash
testapp
    │ ...
    ├─management
    │  │  __init__.py
    │  ├─commands
    │  │  │  seed_users.py
    │  │  │  __init__.py
    │  │  └─__pycache__
    │  └─__pycache__
    │ ...
```

### 2. `setting.py`에 `testapp(앱 폴더명)` 추가

```python
INSTALLED_APPS = (
    ...
    'testapp',
)
```

### 3. 등록되었는지 확인

```bash
python manage.py --help # 명령어 입력
```

```bash
# 올바른 결과
...
[testapp]
    seed_users
...
```

### 4. seed_users.py 작성

[django-seed 공식 깃허브 문서 참조]("https://github.com/Brobin/django-seed?tab=readme-ov-file#usage")

```python
# seed.py 작성 예시
from django_seed import Seed

seeder = Seed.seeder()

from myapp.models import Game, Player
seeder.add_entity(Game, 5)
seeder.add_entity(Player, 10)

inserted_pks = seeder.execute()
```

```python
# 세부적인 data 설정 예시
# 'Player' 모델에 '10'개의 데이터를 넣는데
# 'score'는 1000점 이하로 'nickname'은 faker api를 활용하여 가짜 이메일 데이터 생성
seeder.add_entity(Player, 10, {
    'score':    lambda x: random.randint(0, 1000),
    'nickname': lambda x: seeder.faker.email(),
})
seeder.execute()
```

## 5(final). 사용

```bash
# 현재 작성한 파일 기준
# docs 기준 X
python manage.py seed_users --user=10 --study=5
```

---

# DB(sqlite3) 초기화 하기

## 1. 마이그레이션 파일 삭제하기

- 초기화할 apps안에 있는 migrations 디렉토리 안에 `__init__.py`를 제외한 모든 파일을 지운다.

## 2. 데이터베이스 제거

- db.sqlite3 파일을 날려버린다.

## 3. 새 스키마 생성

```bash
python manage.py makemigrations
python manage.py migrate
```
