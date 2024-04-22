# Generated by Django 3.1 on 2024-01-14 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BookRecommend', '0002_author_book_rating_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'managed': False},
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
        migrations.AddField(
            model_name='userhistory',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BookRecommend.book'),
        ),
        migrations.AddField(
            model_name='userhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
