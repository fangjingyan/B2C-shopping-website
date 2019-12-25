from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField
# Create your models here.


class GoodsType(BaseModel):
    # goods type model class
    name = models.CharField(max_length=20, verbose_name='Type name')
    logo = models.CharField(max_length=20, verbose_name='logo')
    image = models.ImageField(upload_to='type', verbose_name='Type image')

    class Meta:
        db_table = 'df_goods_type'
        verbose_name = 'Goods Type'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsSKU(BaseModel):
    # goods SKU model class
    status_choices = (
        (0, 'out of stock'),
        (1, 'in stock'),
    )
    type = models.ForeignKey('GoodsType', on_delete=models.SET_NULL, null=True, verbose_name='Goods Type')
    goods = models.ForeignKey('Goods', on_delete=models.SET_NULL, null=True, verbose_name='Goods SPU')
    name = models.CharField(max_length=20, verbose_name='Goods Name')
    desc = models.CharField(max_length=256, verbose_name='Goods Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Goods Price')
    unite = models.CharField(max_length=20, verbose_name='Goods Unite')
    image = models.ImageField(upload_to='goods', verbose_name='Goods image')
    stock = models.IntegerField(default=1, verbose_name='Goods Stock')
    sales = models.IntegerField(default=0, verbose_name='Goods Sales')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='Goods Status')

    class Meta:
        db_table = 'df_goods_sku'
        verbose_name = 'Goods'
        verbose_name_plural = verbose_name


class Goods(BaseModel):
    # goods SPU model class
    name = models.CharField(max_length=20, verbose_name='Goods SPU Name')
    # rich text
    detail = HTMLField(blank=True, verbose_name='Goods Detail')

    class Meta:
        db_table = 'df_goods'
        verbose_name = 'Goods SPU'
        verbose_name_plural = verbose_name


class GoodsImage(BaseModel):
    # goods image model class
    sku = models.ForeignKey('GoodsSKU', on_delete=models.SET_NULL, null=True, verbose_name='Goods')
    image = models.ImageField(upload_to='goods', verbose_name='Image Path')

    class Meta:
        db_table = 'df_goods_image'
        verbose_name = 'Goods Image'
        verbose_name_plural = verbose_name


class IndexGoodsBanner(BaseModel):
    # carousel goods model class
    sku = models.ForeignKey('GoodsSKU', on_delete=models.SET_NULL, null=True, verbose_name='Goods')
    image = models.ImageField(upload_to='banner', verbose_name='Image')
    index = models.SmallIntegerField(default=0, verbose_name='Index')

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = 'Index Carousel Goods'
        verbose_name_plural = verbose_name


class IndexTypeGoodsBanner(BaseModel):
    # Type goods model class
    DISPLAY_TYPE_CHOICES = (
        (0, "Title"),
        (1, "Image")
    )

    type = models.ForeignKey('GoodsType', on_delete=models.SET_NULL, null=True, verbose_name='Goods Type')
    sku = models.ForeignKey('GoodsSKU', on_delete=models.SET_NULL, null=True, verbose_name='Goods SKU')
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_TYPE_CHOICES, verbose_name='Display Type')
    index = models.SmallIntegerField(default=0, verbose_name='Index')

    class Meta:
        db_table = 'df_index_type_goods'
        verbose_name = "Index Type Goods"
        verbose_name_plural = verbose_name


class IndexPromotionBanner(BaseModel):
    # promotion model class
    name = models.CharField(max_length=20, verbose_name='Promotion Name')
    url = models.URLField(verbose_name='Promotion Link')
    image = models.ImageField(upload_to='banner', verbose_name='Promotion Image')
    index = models.SmallIntegerField(default=0, verbose_name='Index')

    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = "Index Promotion"
        verbose_name_plural = verbose_name
