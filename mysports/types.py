from graphene_django import DjangoObjectType
from mysports.models import Leagues, Matches, Sports, Teams


class SportType(DjangoObjectType):
    class Meta:
        model = Sports


class LeagueType(DjangoObjectType):
    class Meta:
        model = Leagues


class TeamType(DjangoObjectType):
    class Meta:
        model = Teams


class MatchType(DjangoObjectType):
    class Meta:
        model = Matches