# Generated by Django 5.0.7 on 2024-07-22 09:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_rename_reaction_reaction_reaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='post_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='blog.post'),
        ),
    ]
