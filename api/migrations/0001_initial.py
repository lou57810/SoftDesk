# Generated by Django 4.2 on 2023-05-28 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=1024)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(choices=[('Author', 'Author'), ('Contributor', 'Contributor')], max_length=16)),
                ('role', models.CharField(choices=[('Developpeur Python', 'Developpeur Python'), ('UX-Designer', 'UX-Designer'), ('Administrateur Database', 'Administrateur Database')], max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('desc', models.TextField(max_length=1024)),
                ('tag', models.CharField(choices=[('Bug', 'Bug'), ('Task', 'Task'), ('Enhance', 'Enhance')], max_length=16)),
                ('priority', models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=16)),
                ('status', models.CharField(choices=[('Todo', 'Todo'), ('In progress', 'In progress'), ('Finished', 'Finished')], max_length=16)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=1024)),
                ('type', models.CharField(choices=[('Back-end', 'Back-end'), ('Front-end', 'Front-end'), ('iOS', 'iOS'), ('Android', 'Android')], max_length=16)),
            ],
        ),
    ]
