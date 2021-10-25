# Generated by Django 3.1.3 on 2021-10-25 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InstaPay', '0007_auto_20211025_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloger',
            name='forgot_password_code',
            field=models.IntegerField(default=497286),
        ),
        migrations.AlterField(
            model_name='bloger',
            name='forgot_password_code_deadline',
            field=models.FloatField(default=1635153011.2183216),
        ),
        migrations.AlterField(
            model_name='factor',
            name='factor_id',
            field=models.IntegerField(default=224389119050025168195707713025456716291),
        ),
        migrations.AlterField(
            model_name='offcode',
            name='deadline',
            field=models.FloatField(default=1635153611.640411),
        ),
        migrations.AlterField(
            model_name='offcode',
            name='generating_time',
            field=models.FloatField(default=1635152711.6404397),
        ),
        migrations.AlterField(
            model_name='offcode',
            name='off_code_id',
            field=models.CharField(default='224389118970797005681443375431912765955', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default=None, upload_to='InstaPay/Product_Image/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='off_code_deadline',
            field=models.FloatField(default=1635152711.5859547),
        ),
    ]