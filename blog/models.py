from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):

    #Enum
    class Status (models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'


    title = models.CharField(max_length=250)
    slug = models. SlugField(max_length = 250)
    author = models.ForeignKey(User,
                               on_delete = models.CASCADE,
                               related_name = 'blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)

    status = models.CharField(max_length = 2,
                              choices = Status.choices, 
                              default = Status.DRAFT)

    # latest post channxa ko lagi use bhako orderiing = publish
    #ani indexex le chai page number ni deko ani latest post lauda sabai check garnu bhanda index bta choose garnu sajilo hunxa 
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields = ['-publish']),
        ]

    def __str__(self):
        return self.title
