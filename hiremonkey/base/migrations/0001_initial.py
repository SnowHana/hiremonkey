# Generated by Django 5.1.2 on 2025-01-18 13:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-title'],
            },
        ),
        migrations.CreateModel(
            name='JobSeeker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('title', models.CharField(default='default profile', max_length=200)),
                ('bio', models.TextField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('min_salary', models.FloatField(blank=True, default=0, null=True)),
                ('max_salary', models.FloatField(blank=True, default=0, null=True)),
                ('academics', models.TextField(blank=True, null=True)),
                ('age', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_profiles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated', '-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_date', models.DateTimeField(auto_now_add=True)),
                ('match_status', models.CharField(choices=[('P', 'Pending'), ('A', 'Accepted'), ('D', 'Declined'), ('F', 'Failed')], default='P', max_length=1)),
                ('memo', models.TextField(blank=True, null=True)),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.jobseeker')),
            ],
        ),
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('title', models.CharField(default='default profile', max_length=200)),
                ('bio', models.TextField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('min_salary', models.FloatField(blank=True, default=0, null=True)),
                ('max_salary', models.FloatField(blank=True, default=0, null=True)),
                ('company', models.CharField(max_length=255)),
                ('matches', models.ManyToManyField(related_name='recruiters', through='base.Match', to='base.jobseeker')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_profiles', to=settings.AUTH_USER_MODEL)),
                ('skills', models.ManyToManyField(blank=True, related_name='%(class)s_profiles', to='base.skill')),
            ],
            options={
                'ordering': ['-updated', '-created'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='match',
            name='recruiter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.recruiter'),
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='matches',
            field=models.ManyToManyField(related_name='job_seekers', through='base.Match', to='base.recruiter'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_status', models.CharField(choices=[('J', 'JobSeeker'), ('R', 'Recruiter')], default='J', max_length=1)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('title', models.CharField(default='default profile', max_length=200)),
                ('bio', models.TextField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('min_salary', models.FloatField(blank=True, default=0, null=True)),
                ('max_salary', models.FloatField(blank=True, default=0, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_profiles', to=settings.AUTH_USER_MODEL)),
                ('skills', models.ManyToManyField(blank=True, related_name='%(class)s_profiles', to='base.skill')),
            ],
            options={
                'ordering': ['-updated', '-created'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='%(class)s_profiles', to='base.skill'),
        ),
    ]
