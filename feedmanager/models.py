from django.contrib.auth.models import User
from django.db import models

class Feed(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    description = models.TextField()
    language = models.CharField(max_length=5)
    maximum_length = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def addItem(self, **kw):
        Item.objects.create(feed=self, **kw)


class Item(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    description = models.TextField()
    pubDate = models.DateTimeField()
    feed = models.ForeignKey('Feed', on_delete=models.CASCADE)

    def __str__(self):
        return "%s[%s]" % (self.feed, self.title)
