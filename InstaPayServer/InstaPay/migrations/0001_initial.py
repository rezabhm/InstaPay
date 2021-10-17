# Generated by Django 3.1.3 on 2021-10-17 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bloger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('last_name', models.CharField(max_length=10)),
                ('page_name', models.CharField(max_length=25)),
                ('national_code', models.IntegerField()),
                ('address', models.TextField()),
                ('phone_number', models.CharField(help_text='09121234567', max_length=12)),
                ('bloger_email', models.EmailField(max_length=254)),
                ('bank_account_number', models.CharField(max_length=30)),
                ('bank_name', models.CharField(max_length=15)),
                ('shaba', models.CharField(max_length=50)),
                ('bloger_hashcode', models.CharField(default='19', max_length=15)),
                ('bloger_password_hashcode', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(help_text='09121234567', max_length=12)),
                ('address', models.TextField()),
                ('customer_email', models.EmailField(max_length=254)),
                ('postal_code', models.CharField(max_length=25)),
                ('name', models.CharField(max_length=12)),
                ('last_name', models.CharField(max_length=12)),
                ('bloger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaPay.bloger')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('price', models.IntegerField(help_text='تومان')),
                ('description', models.TextField()),
                ('number', models.IntegerField()),
                ('purchase_state', models.BooleanField(default=True)),
                ('off_code', models.IntegerField(default=0)),
                ('off_code_deadline', models.FloatField(default=1634453254.7177136)),
                ('category', models.CharField(max_length=20)),
                ('product_hashcode', models.CharField(default='29', max_length=128)),
                ('bloger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaPay.bloger')),
            ],
        ),
        migrations.CreateModel(
            name='OffCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('off_code_id', models.CharField(default='37222573164871225158920562902403555121', max_length=50)),
                ('off_number', models.IntegerField()),
                ('deadline', models.FloatField(default=1634454154.7283561)),
                ('generating_time', models.FloatField(default=1634453254.7285569)),
                ('using', models.BooleanField(default=False)),
                ('bloger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaPay.bloger')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaPay.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaPay.product')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('image', models.ImageField(upload_to='product_image/')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='InstaPay.product')),
            ],
        ),
        migrations.CreateModel(
            name='Factor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factor_id', models.IntegerField(default=37222573244099387673184900495947505457)),
                ('customer_payment_year', models.IntegerField()),
                ('customer_payment_month', models.IntegerField()),
                ('customer_payment_day', models.IntegerField()),
                ('customer_payment_hours', models.IntegerField()),
                ('customer_payment_minutes', models.IntegerField()),
                ('factor_statement_ordering_factor', models.BooleanField(default=False)),
                ('factor_statement_payment_to_bloger', models.BooleanField(default=False)),
                ('price', models.IntegerField(help_text='تومان')),
                ('number_of_product', models.IntegerField(default=1)),
                ('delivery_year', models.IntegerField(null=True)),
                ('delivery_month', models.IntegerField(null=True)),
                ('delivery_day', models.IntegerField(null=True)),
                ('delivery_hours', models.IntegerField(null=True)),
                ('delivery_minutes', models.IntegerField(null=True)),
                ('bloger_payment_year', models.IntegerField(null=True)),
                ('bloger_payment_month', models.IntegerField(null=True)),
                ('bloger_payment_day', models.IntegerField(null=True)),
                ('bloger_payment_hours', models.IntegerField(null=True)),
                ('bloger_payment_minutes', models.IntegerField(null=True)),
                ('bloger_payment_bank', models.CharField(max_length=15, null=True)),
                ('bloger_payment_serial', models.CharField(max_length=50, null=True)),
                ('bloger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaPay.bloger')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaPay.customer')),
                ('off_code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='InstaPay.offcode')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaPay.product')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='product',
            field=models.ManyToManyField(to='InstaPay.Product'),
        ),
    ]