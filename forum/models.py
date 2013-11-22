from django.contrib.gis.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from datetime import datetime

class Status(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    shortname = models.CharField(primary_key=True, unique=True, max_length=30)
    description = models.TextField()

    def __unicode__(self):
        return self.name

class Forum(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=300)
    count = models.IntegerField()
    shortname = models.CharField(max_length=30)
    categories = models.ManyToManyField(Category)
    
    class Meta:
        db_table = u'forum'

    def __unicode__(self):
        return self.name
        
class Post(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='replies')
    is_comment = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    heading = models.CharField(max_length=255)
    content = models.TextField(blank=False)
    is_html = models.BooleanField(default=False)
    major = models.BooleanField(default=False)
    post_ip = models.CharField(max_length=255)
    status = models.ForeignKey(Status, default=1)
    hits = models.IntegerField(default=0, blank=True, null=True)
    forum = models.ForeignKey(Forum)
    categories = models.ManyToManyField(Category)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['created']

    class Meta:
        ordering=['tree_id','lft']

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.now()
        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.heading
    


