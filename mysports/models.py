# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BasketballStats(models.Model):
    id = models.BigAutoField(primary_key=True)
    match = models.ForeignKey('Matches', models.DO_NOTHING)
    team = models.ForeignKey('Teams', models.DO_NOTHING)
    fgm = models.SmallIntegerField(db_column='FGM')  # Field name made lowercase.
    fga = models.SmallIntegerField(db_column='FGA', blank=True, null=True)  # Field name made lowercase.
    fg_accuracy = models.SmallIntegerField(db_column='FG_accuracy', blank=True, null=True)  # Field name made lowercase.
    number_3pm = models.SmallIntegerField(db_column='3PM', blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_3pa = models.SmallIntegerField(db_column='3PA', blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_3p_accuracy = models.SmallIntegerField(db_column='3P_accuracy', blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    ftm = models.SmallIntegerField(db_column='FTM', blank=True, null=True)  # Field name made lowercase.
    fta = models.SmallIntegerField(db_column='FTA', blank=True, null=True)  # Field name made lowercase.
    ft_accuracy = models.SmallIntegerField(db_column='FT_accuracy', blank=True, null=True)  # Field name made lowercase.
    oreb = models.SmallIntegerField(blank=True, null=True)
    dreb = models.SmallIntegerField(blank=True, null=True)
    reb = models.SmallIntegerField(blank=True, null=True)
    stl = models.SmallIntegerField(blank=True, null=True)
    blk = models.SmallIntegerField(blank=True, null=True)
    turnover = models.SmallIntegerField(blank=True, null=True)
    foul = models.SmallIntegerField(blank=True, null=True)
    point = models.SmallIntegerField(blank=True, null=True)
    margin = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'basketball_stats'


class FootballStats(models.Model):
    id = models.BigAutoField(primary_key=True)
    match = models.ForeignKey('Matches', models.DO_NOTHING)
    team = models.ForeignKey('Teams', models.DO_NOTHING)
    score = models.SmallIntegerField(blank=True, null=True)
    possesion = models.SmallIntegerField(blank=True, null=True)
    shots = models.SmallIntegerField(blank=True, null=True)
    shots_on_target = models.SmallIntegerField(blank=True, null=True)
    corners = models.SmallIntegerField(blank=True, null=True)
    fouls = models.SmallIntegerField(blank=True, null=True)
    penalties = models.SmallIntegerField(blank=True, null=True)
    yellow_cards = models.SmallIntegerField(blank=True, null=True)
    red_cards = models.SmallIntegerField(blank=True, null=True)
    offsides = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'football_stats'


class Leagues(models.Model):
    id = models.BigAutoField(primary_key=True)
    sport = models.ForeignKey('Sports', models.DO_NOTHING)
    official_site = models.CharField(max_length=50, blank=True, null=True)
    logo_url = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'leagues'


class Lineups(models.Model):
    id = models.BigAutoField(primary_key=True)
    match = models.ForeignKey('Matches', models.DO_NOTHING)
    team = models.ForeignKey('Teams', models.DO_NOTHING)
    formation = models.CharField(max_length=10, blank=True, null=True)
    coach = models.CharField(max_length=30)
    starters = models.TextField()
    substitutes = models.TextField()

    class Meta:
        managed = False
        db_table = 'lineups'


class Matches(models.Model):
    id = models.BigAutoField(primary_key=True)
    league = models.ForeignKey(Leagues, models.DO_NOTHING)
    season = models.ForeignKey('Seasons', models.DO_NOTHING)
    scheduled_date = models.DateTimeField()
    timezone = models.CharField(max_length=5)
    scheduled_date_utc = models.DateTimeField(db_column='scheduled_date_UTC')  # Field name made lowercase.
    away_team = models.ForeignKey('Teams', models.DO_NOTHING, db_column='away_team', related_name='fk_match_away_team')
    home_team = models.ForeignKey('Teams', models.DO_NOTHING, db_column='home_team', related_name='fk_match_home_team')
    location = models.CharField(max_length=30)
    url = models.CharField(unique=True, max_length=200)

    class Meta:
        managed = False
        db_table = 'matches'


class Seasons(models.Model):
    id = models.BigAutoField(primary_key=True)
    start_year = models.SmallIntegerField()
    end_year = models.SmallIntegerField()

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
    league = models.ForeignKey(Leagues, models.DO_NOTHING)
    conference = models.CharField(max_length=10, blank=True, null=True)
    division = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(unique=True, max_length=50, blank=True, null=True)
    short_name = models.CharField(max_length=5, blank=True, null=True)
    official_site = models.CharField(max_length=50, blank=True, null=True)
    logo_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teams'
