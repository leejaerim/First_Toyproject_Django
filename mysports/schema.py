from mysports.types import BasketballStandingType, FootballStandingType, MatchType, CompetitionType, SeasonType
from mysports.models import BasketballStandings, FootballStandings, Matches, Competitions, Seasons
from datetime import datetime
from django.db.models import Q
import graphene
import pytz


class SportQuery(graphene.ObjectType):
    competitions = graphene.List(CompetitionType)
    seasons = graphene.List(SeasonType)
    matches = graphene.List(
        MatchType,
        competitions=graphene.List(graphene.Int, required=False),
        teams=graphene.List(graphene.Int, required=False),
        start_date=graphene.DateTime(required=False),
        end_date=graphene.DateTime(required=False),
    )

    match = graphene.Field(
        MatchType,
        match_id=graphene.Int()
    )

    football_standings = graphene.List(
        FootballStandingType,
        season=graphene.Int()
    )

    basketball_standings = graphene.List(
        BasketballStandingType,
        season=graphene.Int()
    )

    def resolve_competitions(self, info, **kwagrs):
        return Competitions.objects.using('mysports').all()

    def resolve_seasons(self, info, **kwagrs):
        return Seasons.objects.using('mysports').all()

    def resolve_matches(self, info, **kwargs):
        start_date = kwargs.get('start_date') if kwargs.get(
            'start_date') is not None else datetime.utcnow()
        end_date = kwargs.get('end_date') if kwargs.get(
            'end_date') is not None else datetime.utcnow()
        if end_date < start_date:
            raise Exception('Invalid Date Range')

        start_date = start_date.astimezone(pytz.UTC)
        end_date = end_date.astimezone(pytz.UTC)

        teams = kwargs.get('teams')
        competitions = kwargs.get('competitions')
        if teams is not None:
            return Matches.objects.using('mysports').filter(
                scheduled_date_utc__gte=start_date,
                scheduled_date_utc__lte=end_date,
            ).filter(
                Q(home_team__in=teams) | Q(away_team__in=teams)
            ).order_by('scheduled_date_utc')

        elif competitions is not None:
            return Matches.objects.using('mysports').filter(
                scheduled_date_utc__gte=start_date,
                scheduled_date_utc__lte=end_date,
            ).filter(competition__in=competitions).order_by('scheduled_date_utc')

        else:
            return Matches.objects.using('mysports').filter(
                scheduled_date_utc__gte=start_date,
                scheduled_date_utc__lte=end_date,
            ).order_by('scheduled_date_utc')

    def resolve_football_standings(self, info, season):
        return FootballStandings.objects.using('mysports').filter(
            season__id=season
        ).order_by('position')

    def resolve_basketball_standings(self, info, season):
        return BasketballStandings.objects.using('mysports').filter(
            season__id=season
        ).order_by('position')

    def resolve_match(self, info, match_id):
        return Matches.objects.using('mysports').get(pk=match_id)
