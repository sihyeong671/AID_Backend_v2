from django.contrib import admin

from .models import Apply, Comment, Competition, Project, Question, Reply, Study, Tag, User

admin.site.register([User, Study, Project, Competition, Question, Comment, Reply, Tag, Apply])
