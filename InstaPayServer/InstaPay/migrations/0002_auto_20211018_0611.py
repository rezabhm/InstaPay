# Generated by Django 3.1.3 on 2021-10-18 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InstaPay', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloger',
            name='forgot_password_code',
            field=models.IntegerField(default=631766),
        ),
        migrations.AddField(
            model_name='bloger',
            name='forgot_password_code_deadline',
            field=models.FloatField(default=1634537770.8299203),
        ),
        migrations.AlterField(
            model_name='factor',
            name='factor_id',
            field=models.IntegerField(default=65816865153985889254624536590690805205),
        ),
        migrations.AlterField(
            model_name='offcode',
            name='deadline',
            field=models.FloatField(default=1634538372.1748238),
        ),
        migrations.AlterField(
            model_name='offcode',
            name='generating_time',
            field=models.FloatField(default=1634537472.1748493),
        ),
        migrations.AlterField(
            model_name='offcode',
            name='off_code_id',
            field=models.CharField(default='65816865074757726740360198997146854869', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='off_code_deadline',
            field=models.FloatField(default=1634537471.1728835),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_hashcode',
            field=models.CharField(default='31', max_length=128),
        ),
    ]