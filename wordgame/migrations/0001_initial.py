# Generated by Django 4.0.8 on 2024-02-21 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EnglishDictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dictionary', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='MatchList',
            fields=[
                ('channel_name', models.CharField(max_length=200)),
                ('channel_ID', models.IntegerField()),
                ('match_ID', models.AutoField(primary_key=True, serialize=False)),
                ('players_count', models.IntegerField(blank=True, null=True)),
                ('word_count', models.IntegerField(blank=True, null=True)),
                ('queue', models.PositiveIntegerField(default=1)),
                ('start_game', models.BooleanField(default=False)),
                ('finished', models.BooleanField(default=False)),
                ('progress', models.CharField(default='no active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='GamersList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_ID', models.IntegerField(blank=True, null=True)),
                ('user_id', models.IntegerField()),
                ('user_name', models.CharField(max_length=200)),
                ('found_word_count', models.IntegerField(blank=True, null=True)),
                ('chance', models.IntegerField(default=3)),
                ('queue', models.PositiveIntegerField(default=1)),
                ('start_game', models.BooleanField(default=False)),
                ('finished', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('Match_List', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wordgame.matchlist')),
            ],
        ),
        migrations.CreateModel(
            name='ChempionsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_ID', models.IntegerField(blank=True, null=True)),
                ('channel_name', models.CharField(max_length=200)),
                ('channel_ID', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('user_name', models.CharField(max_length=100)),
                ('results', models.IntegerField()),
                ('MatchList', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wordgame.matchlist')),
            ],
        ),
    ]