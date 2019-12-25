from django.db import models


class BaseModel(models.Model):

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Create time')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='Update time')
    is_delete = models.BooleanField(default=False, verbose_name='Delete sign')

    class Meta:
        # This is an abstract model class
        abstract = True
