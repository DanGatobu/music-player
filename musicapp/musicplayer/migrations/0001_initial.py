# Generated by Django 4.1.5 on 2023-02-06 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='songs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('album', models.CharField(max_length=200)),
                ('artist', models.CharField(max_length=200)),
                ('length', models.DurationField()),
                ('link', models.FileField(upload_to='music/')),
            ],
        ),
    ]