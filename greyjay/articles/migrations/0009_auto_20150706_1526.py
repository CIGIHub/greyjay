# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_auto_20150702_1954'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlecategory',
            options={'verbose_name_plural': 'Article Categories'},
        ),
    ]
