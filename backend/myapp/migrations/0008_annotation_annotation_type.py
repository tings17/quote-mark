# Generated by Django 5.1.6 on 2025-03-05 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_annotation_author_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='annotation_type',
            field=models.TextField(blank=True),
        ),
    ]
