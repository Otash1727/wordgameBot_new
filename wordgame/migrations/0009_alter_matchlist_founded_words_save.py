# Generated by Django 4.0.8 on 2024-02-24 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordgame', '0008_rename_founded_words2_matchlist_founded_words_save'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchlist',
            name='founded_words_save',
            field=models.CharField(blank=True, default='1', max_length=10000, null=True),
        ),
    ]
