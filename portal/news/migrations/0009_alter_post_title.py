# Generated by Django 4.1.6 on 2023-02-12 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_alter_post_options_category_create_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='статья от 2023-02-12 02:23:04.197527', max_length=64),
        ),
    ]
