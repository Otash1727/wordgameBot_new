# Generated by Django 4.0.8 on 2024-02-24 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordgame', '0003_matchlist_founded_words'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchlist',
            name='founded_words',
            field=models.CharField(blank=True, default='1', max_length=3000, null=True),
        ),
    ]
