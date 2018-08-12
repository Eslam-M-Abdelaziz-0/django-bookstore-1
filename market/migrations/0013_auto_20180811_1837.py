# Generated by Django 2.1 on 2018-08-11 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('market', '0012_auto_20180811_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivationLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('link', models.CharField(max_length=36)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='activationlinks',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.AlterField(
            model_name='book',
            name='holders',
            field=models.ManyToManyField(blank=True, editable=False, related_name='books', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='book',
            name='shoppers',
            field=models.ManyToManyField(blank=True, editable=False, related_name='shopping_cart', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='ActivationLinks',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
