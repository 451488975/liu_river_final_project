from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse


class Period(models.Model):
    period_id = models.AutoField(primary_key=True)
    period_sequence = models.IntegerField(unique=True)
    period_name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return f'{self.period_name}'

    class Meta:
        ordering = ['period_sequence']


class Year(models.Model):
    year_id = models.AutoField(primary_key=True)
    year = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.year}'

    class Meta:
        ordering = ['year']


class Position(models.Model):
    position_id = models.AutoField(primary_key=True)
    position_sequence = models.IntegerField(unique=True)
    position_name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return f'{self.position_name}'

    class Meta:
        ordering = ['position_sequence']


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=100)
    website = models.CharField(max_length=255, default='')
    developer = models.CharField(max_length=100, default='')
    developer_website = models.CharField(max_length=255, default='')
    genre = models.CharField(max_length=45)

    def __str__(self):
        return f'{self.game_name}'

    def get_absolute_url(self):
        return reverse(
            'proleague_game_detail_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_update_url(self):
        return reverse(
            'proleague_game_update_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_delete_url(self):
        return reverse(
            'proleague_game_delete_urlpattern',
            kwargs={'pk': self.pk}
        )

    class Meta:
        ordering = ['game_name']
        constraints = [
            UniqueConstraint(fields=['game_name', 'genre'], name='unique_game')
        ]


class Tournament(models.Model):
    tournament_id = models.AutoField(primary_key=True)
    tournament_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    year = models.ForeignKey(Year, related_name='tournaments', on_delete=models.PROTECT)
    period = models.ForeignKey(Period, related_name='tournaments', on_delete=models.PROTECT)
    game = models.ForeignKey(Game, related_name='tournaments', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.tournament_name}'

    def get_absolute_url(self):
        return reverse(
            'proleague_tournament_detail_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_update_url(self):
        return reverse(
            'proleague_tournament_update_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_delete_url(self):
        return reverse(
            'proleague_tournament_delete_urlpattern',
            kwargs={'pk': self.pk}
        )

    class Meta:
        ordering = ['year__year', 'period__period_sequence', 'start_date', 'end_date']
        constraints = [
            UniqueConstraint(fields=['year', 'period', 'tournament_name'], name='unique_tournament')
        ]


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=45)
    acronym = models.CharField(max_length=45, unique=True)
    tournament = models.ForeignKey(Tournament, related_name='teams', on_delete=models.PROTECT)
    position = models.ForeignKey(
        Position, related_name='teams', on_delete=models.PROTECT, null=True, blank=True
    )

    def __str__(self):
        return f'{self.team_name}({self.acronym})'

    def get_absolute_url(self):
        return reverse(
            'proleague_team_detail_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_update_url(self):
        return reverse(
            'proleague_team_update_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_delete_url(self):
        return reverse(
            'proleague_team_delete_urlpattern',
            kwargs={'pk': self.pk}
        )

    class Meta:
        ordering = ['team_name']
        constraints = [
            UniqueConstraint(fields=['team_name', 'tournament'], name='unique_team')
        ]


class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    match_type = models.CharField(max_length=100)
    match_time = models.DateTimeField()
    duration = models.CharField(max_length=45)
    team_a = models.ForeignKey(Team, related_name='match_a', on_delete=models.PROTECT)
    team_b = models.ForeignKey(Team, related_name='match_b', on_delete=models.PROTECT)
    match_detail = models.TextField()
    video_link = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.team_a.tournament} - [{self.match_type}] {self.team_a.acronym} VS. {self.team_b.acronym}'

    def get_absolute_url(self):
        return reverse(
            'proleague_match_detail_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_update_url(self):
        return reverse(
            'proleague_match_update_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_delete_url(self):
        return reverse(
            'proleague_match_delete_urlpattern',
            kwargs={'pk': self.pk}
        )

    class Meta:
        ordering = ['team_a__tournament', 'match_time']
        constraints = [
            UniqueConstraint(fields=['match_type', 'team_a', 'team_b'], name='unique_match')
        ]


class School(models.Model):
    school_id = models.AutoField(primary_key=True)
    school_name = models.CharField(max_length=255)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)

    def __str__(self):
        return f'{self.school_name}'

    def get_absolute_url(self):
        return reverse(
            'proleague_school_detail_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_update_url(self):
        return reverse(
            'proleague_school_update_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_delete_url(self):
        return reverse(
            'proleague_school_delete_urlpattern',
            kwargs={'pk': self.pk}
        )

    class Meta:
        ordering = ['school_name']
        constraints = [
            UniqueConstraint(fields=['school_name', 'city', 'state'], name='unique_school')
        ]


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    player_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    gamer_tag = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=45)
    school = models.ForeignKey(School, related_name='players', on_delete=models.PROTECT)
    team = models.ForeignKey(Team, related_name='players', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.player_name}({self.gamer_tag})'

    def get_absolute_url(self):
        return reverse(
            'proleague_player_detail_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_update_url(self):
        return reverse(
            'proleague_player_update_urlpattern',
            kwargs={'pk': self.pk}
        )

    def get_delete_url(self):
        return reverse(
            'proleague_player_delete_urlpattern',
            kwargs={'pk': self.pk}
        )

    class Meta:
        ordering = ['player_name', 'gamer_tag']
        constraints = [
            UniqueConstraint(fields=['player_name', 'gamer_tag'], name='unique_player')
        ]
