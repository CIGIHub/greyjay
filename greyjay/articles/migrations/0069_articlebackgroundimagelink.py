# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20150923_1943'),
        ('articles', '0067_auto_20151005_2045'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleBackgroundImageLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article', modelcluster.fields.ParentalKey(related_name='background_image_links', to='articles.ArticlePage')),
                ('background_image', models.ForeignKey(related_name='+', to='images.AttributedImage')),
            ],
        ),
    ]
