# Generated by Django 4.1.6 on 2023-02-11 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='статья от 2023-02-11 14:39:22.356110', max_length=64),
        ),
    ]