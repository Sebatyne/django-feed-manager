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

    def deleteOldItems(self):
        item_list = Item.objects \
                        .filter(feed=self) \
                        .order_by('pubDate')
        for i in range(len(item_list) - self.maximum_length):
            item_list[i].delete()

    def addItem(self, **kw):
        Item.objects.create(feed=self, **kw)
        if Item.objects.filter(feed=self).count() > self.maximum_length:
            self.deleteOldItems()

class Item(models.Model):
    PROPERTY_LIST = ['title', 'link', 'description', 'pubDate']

    title = models.CharField(max_length=100)
    link = models.URLField()
    description = models.TextField()
    pubDate = models.DateTimeField()
    feed = models.ForeignKey('Feed', on_delete=models.CASCADE)

    def __str__(self):
        return "%s[%s]" % (self.feed, self.title)
