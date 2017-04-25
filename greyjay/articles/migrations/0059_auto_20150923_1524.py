# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0058_auto_20150904_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlelistpage',
            name='filter',
            field=models.TextField(blank=True, null=True, choices=[('visualizations', 'Visualizations'), ('interviews', 'Interviews'), ('editors_pick', "Editor's Pick"), ('most_popular', 'Most Popular')]),
        ),
    ]
