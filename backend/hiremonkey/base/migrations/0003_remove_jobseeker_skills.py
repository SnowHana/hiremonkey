# Generated by Django 4.1 on 2024-08-26 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_skill_alter_profilereference_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobseeker',
            name='skills',
        ),
    ]
