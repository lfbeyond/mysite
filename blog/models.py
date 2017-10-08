from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Article(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

from django.db import models
from django.conf import settings
class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    image = models.ImageField(upload_to='static/image/%Y/%m', default='static/image/default.jpg', max_length=200,
                              blank=True, null=True, verbose_name='用户头像')
    created_dt = models.DateTimeField(auto_now_add=True, db_index=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.user.username