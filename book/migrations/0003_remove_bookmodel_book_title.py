# Generated by Django 5.0.6 on 2024-08-14 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_rename_body_commentmodel_comment_body_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmodel',
            name='book_title',
        ),
    ]
