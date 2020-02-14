# Generated by Django 3.0.3 on 2020-02-14 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rack',
            name='student_object',
        ),
        migrations.AddField(
            model_name='rack',
            name='student_object',
            field=models.ManyToManyField(blank=True, to='rest.Student'),
        ),
        migrations.RemoveField(
            model_name='student',
            name='rack_obj',
        ),
        migrations.AddField(
            model_name='student',
            name='rack_obj',
            field=models.ManyToManyField(blank=True, to='rest.Rack'),
        ),
    ]
