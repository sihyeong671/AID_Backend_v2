# Create your models here.
from django.db import models
from django.db.models import Model


class User(models.Model):
    nickname = models.CharField(max_length=20)
    email = models.EmailField(max_length=45, unique=True)
    password = models.CharField(max_length=45)
    is_admin = models.BooleanField()
    created_at = models.DateTimeField(auto_now=True)


# Difference between CharField() & TextField() - Q & A
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

# ------------------------------------------------------------------ #

# (fields.E304) Reverse accessor - Q & A:
# Link: https://stackoverflow.com/questions/41595364/fields-e304-reverse-accessor-clashes-in-django

# Q:
# from django.db import models
# class Person(models.Model):
#    name = models.CharField(max_length=64)
# class Person2Person(models.Model):
#    person = models.ForeignKey(Person)
#    friend = models.ForeignKey(Person)

# A:
# The code is wrong because Person will get a reverse relationship back to Person2Person.person,
# and also to Person2Person.friend; the default name would be Person.person2person_set
# but Django can't use the same name for both.

# So you could set a related_name on either, or both:

# class Person2Person(models.Model):
#    person = models.ForeignKey(Person, related_name='person2persons')
#    friend = models.ForeignKey(Person, related_name='friends')

# Now Person.friend's related to the Person2Person objects that have this Person as a friend,
#    and Person.person2person to the ones that have this Person as a person.
# However, why aren't you using a ManyToManyField to 'self' on Person?


class Study(Model):
    study_name = models.CharField(max_length=50)
    study_description = models.CharField(max_length=300)
    study_link = models.CharField(max_length=500, null=True)
    status = models.IntegerField()
    leader_id = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="leader", null=True)
    users = models.ManyToManyField(User, related_name="participants")
    img_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)


class Project(Model):
    project_name = models.CharField(max_length=45)
    project_description = models.TextField()
    project_link = models.CharField(max_length=500, null=True)
    status = models.IntegerField()
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now=True)


class Competition(Model):
    competition_name = models.CharField(max_length=45)
    competition_description = models.TextField()
    competition_link = models.CharField(max_length=500, null=True)
    status = models.IntegerField()
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now=True)


# ManytoOneField - Q & A
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
    writer_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=45)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)


# "on delete cascade"는 B tuple이 foreign key로 A tuple을 가리키고 있을 때, A tuple을 삭제하면 B tuple도 같이 삭제되는 기능이다.
# Link: https://technote.kr/197 [TechNote.kr:티스토리]
class Comment(Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    writer_id = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)


class Reply(Model):
    writer_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    comment_id = models.ForeignKey(Comment, on_delete=models.DO_NOTHING)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)


class Tag(Model):
    tag = models.CharField(max_length=45)
    questions = models.ManyToManyField(Question)


class Apply(Model):
    name = models.CharField(max_length=40)
    email = models.TextField(unique=True)
    student_id = models.TextField(unique=True)
    phone_number = models.CharField(max_length=11)
    motive = models.CharField(max_length=500)
    github_link = models.TextField()
    blog_link = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
