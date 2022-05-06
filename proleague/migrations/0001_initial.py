# Generated by Django 3.2.5 on 2022-05-06 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_id', models.AutoField(primary_key=True, serialize=False)),
                ('game_name', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=45)),
            ],
            options={
                'ordering': ['game_name'],
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('match_id', models.AutoField(primary_key=True, serialize=False)),
                ('match_type', models.CharField(max_length=100)),
                ('match_time', models.DateTimeField()),
                ('duration', models.TimeField()),
                ('match_detail', models.TextField()),
                ('video_link', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['match_time'],
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('period_id', models.AutoField(primary_key=True, serialize=False)),
                ('period_sequence', models.IntegerField(unique=True)),
                ('period_name', models.CharField(max_length=45, unique=True)),
            ],
            options={
                'ordering': ['period_sequence'],
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.AutoField(primary_key=True, serialize=False)),
                ('player_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=255)),
                ('gamer_tag', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=45)),
            ],
            options={
                'ordering': ['player_name', 'gamer_tag'],
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('position_id', models.AutoField(primary_key=True, serialize=False)),
                ('position_sequence', models.IntegerField(unique=True)),
                ('position_name', models.CharField(max_length=45, unique=True)),
            ],
            options={
                'ordering': ['position_sequence'],
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('school_id', models.AutoField(primary_key=True, serialize=False)),
                ('school_name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=45)),
                ('state', models.CharField(max_length=45)),
            ],
            options={
                'ordering': ['school_name'],
            },
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('year_id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.IntegerField(unique=True)),
            ],
            options={
                'ordering': ['year'],
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('tournament_id', models.AutoField(primary_key=True, serialize=False)),
                ('tournament_name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tournaments', to='proleague.game')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tournaments', to='proleague.period')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tournaments', to='proleague.year')),
            ],
            options={
                'ordering': ['year__year', 'period__period_sequence', 'start_date', 'end_date'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.AutoField(primary_key=True, serialize=False)),
                ('team_name', models.CharField(max_length=45)),
                ('acronym', models.CharField(max_length=45, unique=True)),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='teams', to='proleague.position')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teams', to='proleague.tournament')),
            ],
            options={
                'ordering': ['team_name'],
            },
        ),
        migrations.AddConstraint(
            model_name='school',
            constraint=models.UniqueConstraint(fields=('school_name', 'city', 'state'), name='unique_school'),
        ),
        migrations.AddField(
            model_name='player',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='players', to='proleague.school'),
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='players', to='proleague.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team_a',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='match_a', to='proleague.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team_b',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='match_b', to='proleague.team'),
        ),
        migrations.AddConstraint(
            model_name='game',
            constraint=models.UniqueConstraint(fields=('game_name', 'genre'), name='unique_game'),
        ),
        migrations.AddConstraint(
            model_name='tournament',
            constraint=models.UniqueConstraint(fields=('year', 'period', 'tournament_name'), name='unique_tournament'),
        ),
        migrations.AddConstraint(
            model_name='team',
            constraint=models.UniqueConstraint(fields=('team_name', 'tournament'), name='unique_team'),
        ),
        migrations.AddConstraint(
            model_name='player',
            constraint=models.UniqueConstraint(fields=('player_name', 'gamer_tag'), name='unique_player'),
        ),
        migrations.AddConstraint(
            model_name='match',
            constraint=models.UniqueConstraint(fields=('match_type', 'team_a', 'team_b'), name='unique_match'),
        ),
    ]
