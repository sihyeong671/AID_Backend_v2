from django.db import models


class News(models.Model):
    image = models.ImageField(upload_to="news_image/", default=None)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
