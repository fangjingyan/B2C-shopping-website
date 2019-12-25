from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel
# Create your models here.


class User(AbstractUser, BaseModel):
    # user model class

    class Meta:
        db_table = 'df_user'
        verbose_name = 'User'
        verbose_name_plural = verbose_name


class AddressManager(models.Manager):
    # address model manager class

    def get_default_address(self, user):
        # get user default receive address
        # self.model: get self object model class
        try:
            address = self.model.objects.get(user=user, is_default=True)
        except self.model.DoesNotExist:
            # default receive address not exist
            address = None

        return address


class Address(BaseModel):
    # address model class
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, verbose_name='User')
    receiver = models.CharField(max_length=20, verbose_name='Receiver')
    addr = models.CharField(max_length=256, verbose_name='Receive Address')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='Zip Code')
    phone = models.CharField(max_length=11, verbose_name='Cell Phone')
    is_default = models.BooleanField(default=False, verbose_name='Default sign')

    objects = AddressManager()

    class Meta:
        db_table = 'df_address'
        verbose_name = 'Address'
        verbose_name_plural = verbose_name
