from mysports.types import MatchType
from mysports.models import Matches
from datetime import datetime
from django.db.models import Q
import graphene
import pytz


class StandingQuery(graphene.ObjectType):
    pass


class MatchQuery(graphene.ObjectType):
    matches = graphene.List(
        MatchType,
        league_ids=graphene.List(graphene.Int, required=False),
        team_ids=graphene.List(graphene.Int, required=False),
        season_id=graphene.Int(required=False),
        start_date=graphene.DateTime(required=False),
        end_date=graphene.DateTime(required=False),
    )

    def resolve_matches(self, info, **kwargs):
        season_id = kwargs.get('season_id') if kwargs.get(
            'season_id') is not None else 1
        start_date = kwargs.get('start_date') if kwargs.get(
            'start_date') is not None else datetime.utcnow()
        end_date = kwargs.get('end_date') if kwargs.get(
            'end_date') is not None else datetime.utcnow()
        if end_date < start_date:
            raise Exception('Invalid Date Range')

        start_date = start_date.astimezone(pytz.UTC)
        end_date = end_date.astimezone(pytz.UTC)

        team_ids = kwargs.get('team_ids')
        league_ids = kwargs.get('league_ids')
        if team_ids is not None:
            return Matches.objects.using('mysports').filter(
                season_id=season_id,
                scheduled_date_utc__gte=start_date,
                scheduled_date_utc__lte=end_date,
            ).filter(
                Q(home_team__in=team_ids) | Q(away_team__in=team_ids)
            ).order_by('scheduled_date_utc')

        elif league_ids is not None:
            return Matches.objects.using('mysports').filter(
                season_id=season_id,
                scheduled_date_utc__gte=start_date,
                scheduled_date_utc__lte=end_date,
            ).filter(league__in=league_ids).order_by('scheduled_date_utc')

        else:
            return Matches.objects.using('mysports').filter(
                season_id=season_id,
                scheduled_date_utc__gte=start_date,
                scheduled_date_utc__lte=end_date,
            ).order_by('scheduled_date_utc')
