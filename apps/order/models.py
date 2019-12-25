from django.db import models
from db.base_model import BaseModel
# Create your models here.


class OrderInfo(BaseModel):
    # order model class

    PAY_METHOD_CHOICES = (
        (1, 'Cash on delivery'),
        (2, 'Mastercard'),
        (3, 'Visa'),
        (4, 'AmericanExpress')
    )

    ORDER_STATUS_CHOICES = (
        (1, 'UNPAID'),
        (2, 'UNSEND'),
        (3, 'UNRECEIVED'),
        (4, 'UNCOMMENT'),
        (5, 'FINISHED')
    )

    order_id = models.CharField(max_length=128, primary_key=True, verbose_name='Order id')
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, verbose_name='User')
    addr = models.ForeignKey('user.Address', on_delete=models.SET_NULL, null=True, verbose_name='Address')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=3, verbose_name='Pay Method')
    total_count = models.IntegerField(default=1, verbose_name='Goods Count')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Goods Price')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Delivery Price')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='Order Status')
    trade_no = models.CharField(max_length=128, default='', verbose_name='Trade Number')

    class Meta:
        db_table = 'df_order_info'
        verbose_name = 'Order'
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    # order goods model class
    order = models.ForeignKey('OrderInfo', on_delete=models.SET_NULL, null=True, verbose_name='Order')
    sku = models.ForeignKey('goods.GoodsSKU', on_delete=models.SET_NULL, null=True, verbose_name='Goods SKU')
    count = models.IntegerField(default=1, verbose_name='Goods Count')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Gods Price')
    comment = models.CharField(max_length=256, default='', verbose_name='Comment')

    class Meta:
        db_table = 'df_order_goods'
        verbose_name = 'Order Goods'
        verbose_name_plural = verbose_name
