from graphene_django import DjangoObjectType
from mysports.models import BasketballStandings, Competitions, FootballStandings, Matches, Seasons, Sports, Teams


class SportType(DjangoObjectType):
    class Meta:
        model = Sports


class SeasonType(DjangoObjectType):
    class Meta:
        model = Seasons


class CompetitionType(DjangoObjectType):
    class Meta:
        model = Competitions


class TeamType(DjangoObjectType):
    class Meta:
        model = Teams


class MatchType(DjangoObjectType):
    class Meta:
        model = Matches


class FootballStandingType(DjangoObjectType):
    class Meta:
        model = FootballStandings


class BasketballStandingType(DjangoObjectType):
    class Meta:
        model = BasketballStandings

