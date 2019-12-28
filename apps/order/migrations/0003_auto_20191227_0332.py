# Generated by Django 2.1.7 on 2019-12-27 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20191224_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_method',
            field=models.SmallIntegerField(choices=[(1, 'Cash on delivery'), (2, 'WechatPay'), (3, 'AliPay'), (4, 'UnionPay')], default=3, verbose_name='Pay Method'),
        ),
    ]