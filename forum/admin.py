from django.contrib import admin
from mptt.admin import MPTTModelAdmin
import models
import django

admin.site.register(models.Post, MPTTModelAdmin)

for o_name in dir(models):
    o = getattr(models, o_name)
    if hasattr(o, '__class__'):
        if o.__class__ == django.db.models.base.ModelBase:
            try:
                admin.site.register(o)
            except:
                pass
