# Generated by Django 3.1.3 on 2021-11-22 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InstaPay', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloger',
            name='forgot_password_code',
            field=models.IntegerField(default=315799),
        ),
        migrations.AlterField(
            model_name='bloger',
            name='forgot_password_code_deadline',
            field=models.FloatField(default=1637596140.74796),
        ),
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.IntegerField(default=4358745465413015683805907917572371117, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(help_text='09121234567', max_length=25),
        ),
        migrations.AlterField(
            model_name='customer',
            name='product',
            field=models.ManyToManyField(to='InstaPay.Product'),
        ),
        migrations.AlterField(
            model_name='factor',
            name='create_time',
            field=models.FloatField(default=1637595840.8215563),
        ),
        migrations.AlterField(
            model_name='factor',
            name='factor_id',
            field=models.IntegerField(default=4358745623869340712334583104660271789),
        ),
        migrations.AlterField(
            model_name='offcode',
            name='deadline',
            field=models.FloatField(default=1637596740.8204918),
        ),
        migrations.AlterField(
            model_name='offcode',
            name='generating_time',
            field=models.FloatField(default=1637595840.8205273),
        ),
        migrations.AlterField(
            model_name='offcode',
            name='off_code_id',
            field=models.CharField(default='4358745544641178198070245511116321453', max_length=50),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_time',
            field=models.FloatField(default=1637595840.8269384),
        ),
        migrations.AlterField(
            model_name='pending',
            name='pending_time',
            field=models.FloatField(default=1637595840.8235376),
        ),
        migrations.AlterField(
            model_name='product',
            name='off_code_deadline',
            field=models.FloatField(default=4244650056983433.0),
        ),
        migrations.AlterField(
            model_name='samanpayment',
            name='payment_time',
            field=models.FloatField(default=1637595840.8278463),
        ),
    ]
