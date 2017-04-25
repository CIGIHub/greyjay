# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0002_add_verbose_names'),
        ('wagtailcore', '0019_verbose_names_cleanup'),
        ('wagtailforms', '0002_add_verbose_names'),
        ('articles', '0064_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapteredarticlepage',
            name='articlepage_ptr',
        ),
        migrations.DeleteModel(
            name='ChapteredArticlePage',
        ),
    ]
