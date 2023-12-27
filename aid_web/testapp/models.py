# Create your models here.
from django.db import models
from django.db.models import Model


# Ref : https://velog.io/@jewon119/Django-%EA%B8%B0%EC%B4%88-%EB%AA%A8%EB%8D%B8Model-%EA%B4%80%EB%A6%AC%EC%9E%90admin
class User(models.Model):
    nickname = models.CharField(max_length=20)
    email = models.EmailField(max_length=45, unique=True)
    password = models.CharField(max_length=45)
    is_admin = models.BooleanField()
    created_at = models.DateTimeField(auto_now=True)


# Difference between CharField() & TextField() Q & A
# Link: https://stackoverflow.com/questions/7354588/whats-the-difference-between-charfield-and-textfield-in-django

# Q:
# The documentation says that CharField() should be used for smaller strings
# and TextField() should be used for larger strings.

# A:
# PostgreSQL 9, specifically, states that
# "There is no performance difference among these three types",
# but AFAIK there are some differences in e.g. MySQL,
# so this is something to keep in mind.


# A good rule of thumb is that you use CharField when you need to limit the maximum length, TextField otherwise.
class Study(Model):
    study_name = models.CharField(max_length=50)
    # CharField()? TextField()?
    study_description = models.CharField(max_length=300)
    study_link = models.CharField(max_length=500, null=True)
    status = models.IntegerField()
    leader_id = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name="leader")
    users = models.ManyToManyField(User)
    img_url = models.CharField(max_length=100)


class Project(Model):
    project_name = models.CharField(max_length=45)
    project_description = models.TextField()
    project_link = models.CharField(max_length=500, null=True)
    status = models.IntegerField()
    users = models.ManyToManyField(User)


class Competition(Model):
    competition_name = models.CharField(max_length=45)
    competition_description = models.TextField()
    competition_link = models.CharField(max_length=500, null=True)
    status = models.IntegerField()
    users = models.ManyToManyField(User)


# ManytoOneField Q & A
# Link: https://stackoverflow.com/questions/888550/manytoonefield-in-django

# Q:
# class User(models.Model):
# name = models.CharField()

# class Group(models.Model):
# name = models.CharField()
# This is what I want to do -> users = models.ManyToOneField(User)

# ---------------------------------------------------------------- #

# A:
# A ManyToOne field, as you've guessed, is called ForeignKey in Django.
# You will have to define it on your User class for the logic to work properly,
# but Django will make a reverse property available on the Groups model automatically:

# class Group(models.Model):
#   name = models.CharField(max_length=64)

# class User(models.Model):
#   name = models.CharField(max_length=64)
#   group = models.ForeignKey(Group)


# g = Group.objects.get(id=1)
# print g.user_set.all()  # prints list of all users in the group
class Question(Model):
    writer_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=45)
    content = models.TextField()


# "on delete cascade"는 B tuple이 foreign key로 A tuple을 가리키고 있을 때, A tuple을 삭제하면 B tuple도 같이 삭제되는 기능이다.
# 출처: https://technote.kr/197 [TechNote.kr:티스토리]
class Comment(Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    writer_id = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()


class Reply(Model):
    writer_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment_id = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    content = models.TextField()


class Tag(Model):
    tag = models.CharField(max_length=45)
    questions = models.ManyToManyField(Question)


class Apply(Model):
    name = models.CharField(max_length=40)
    email = models.TextField(unique=True)
    student_id = models.TextField(unique=True)
    phone_number = models.CharField(max_length=30)
    motive = models.TextField()
    github = models.TextField()
    blog = models.TextField()
