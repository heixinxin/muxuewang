# Generated by Django 2.1.7 on 2019-03-13 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(default='', max_length=300, verbose_name='老师告诉你'),
        ),
        migrations.AddField(
            model_name='course',
            name='youneed_konw',
            field=models.CharField(default='', max_length=300, verbose_name='课程须知'),
        ),
    ]
