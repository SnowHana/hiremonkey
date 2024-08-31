# Generated by Django 4.1 on 2024-08-31 14:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_skill_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='skill_level',
            field=models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('Expert', 'Expert')], default='Beginner', help_text='Proficiency level of the skill', max_length=20),
        ),
        migrations.AddField(
            model_name='skill',
            name='years_of_experience',
            field=models.PositiveIntegerField(blank=True, help_text='Number of years with this skill', null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]