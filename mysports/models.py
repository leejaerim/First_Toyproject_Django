# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BasketballStandings(models.Model):
    id = models.BigIntegerField(primary_key=True)
    season = models.ForeignKey('Seasons', models.DO_NOTHING)
    team = models.ForeignKey('Teams', models.DO_NOTHING)
    division = models.CharField(max_length=10, blank=True, null=True)
    position = models.SmallIntegerField(blank=True, null=True)
    won = models.SmallIntegerField(blank=True, null=True)
    lost = models.SmallIntegerField(blank=True, null=True)
    win_percentage = models.SmallIntegerField(blank=True, null=True)
    games_behind = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'basketball_standings'


class Competitions(models.Model):
    id = models.BigAutoField(primary_key=True)
    sport = models.ForeignKey('Sports', models.DO_NOTHING)
    name = models.CharField(max_length=50, blank=True, null=True)
    short_name = models.CharField(max_length=20, blank=True, null=True)
    official_site = models.TextField(blank=True, null=True)
    logo_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competitions'


class FootballStandings(models.Model):
    id = models.BigIntegerField(primary_key=True)
    season = models.ForeignKey('Seasons', models.DO_NOTHING)
    team = models.ForeignKey('Teams', models.DO_NOTHING)
    division = models.CharField(max_length=15, blank=True, null=True)
    position = models.SmallIntegerField(blank=True, null=True)
    points = models.SmallIntegerField(blank=True, null=True)
    played = models.SmallIntegerField(blank=True, null=True)
    won = models.SmallIntegerField(blank=True, null=True)
    drawn = models.SmallIntegerField(blank=True, null=True)
    lost = models.SmallIntegerField(blank=True, null=True)
    goals_for = models.SmallIntegerField(blank=True, null=True)
    goals_against = models.SmallIntegerField(blank=True, null=True)
    goal_difference = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'football_standings'


class Matches(models.Model):
    id = models.BigAutoField(primary_key=True)
    season = models.ForeignKey('Seasons', models.DO_NOTHING)
    competition = models.ForeignKey(Competitions, models.DO_NOTHING)
    stage = models.CharField(max_length=20, blank=True, null=True)
    game_number = models.SmallIntegerField(blank=True, null=True)
    scheduled_date = models.DateTimeField()
    timezone = models.CharField(max_length=5)
    scheduled_date_utc = models.DateTimeField(db_column='scheduled_date_UTC')  # Field name made lowercase.
    away_team = models.ForeignKey('Teams', models.DO_NOTHING, db_column='away_team', related_name='fk_away')
    home_team = models.ForeignKey('Teams', models.DO_NOTHING, db_column='home_team', related_name='fk_home')
    location = models.CharField(max_length=30)
    url = models.CharField(unique=True, max_length=200)
    match_status = models.SmallIntegerField(blank=True, null=True)
    match_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matches'


class Seasons(models.Model):
    id = models.BigAutoField(primary_key=True)
    competition = models.ForeignKey(Competitions, models.DO_NOTHING)
    previous_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'seasons'


class Sports(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'sports'


class Teams(models.Model):
    id = models.BigAutoField(primary_key=True)
    sport = models.ForeignKey(Sports, models.DO_NOTHING)
    name = models.CharField(unique=True, max_length=50, blank=True, null=True)
    short_name = models.CharField(max_length=5, blank=True, null=True)
    official_site = models.TextField(blank=True, null=True)
    logo_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teams'
