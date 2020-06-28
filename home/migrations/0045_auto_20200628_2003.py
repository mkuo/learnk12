# Generated by Django 3.0.5 on 2020-06-28 20:03

from django.db import migrations
import modelcluster.contrib.taggit


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('home', '0044_auto_20200620_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursepage',
            name='lesson_type_tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', related_name='lesson_types', through='home.LessonType', to='taggit.Tag', verbose_name='lesson types'),
        ),
        migrations.AlterField(
            model_name='coursepage',
            name='platform_tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', related_name='platforms', through='home.Platform', to='taggit.Tag', verbose_name='platforms'),
        ),
        migrations.AlterField(
            model_name='coursepage',
            name='programming_language_tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', related_name='programming_languages', through='home.ProgrammingLanguage', to='taggit.Tag', verbose_name='programming languages'),
        ),
    ]
