import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Anime, Vote


#1
class AnimeFilter(django_filters.FilterSet):
    class Meta:
        model = Anime
        fields = ['name', 'episode_count', 'season_count', 'status', 'description', 'studio']


#2
class AnimeNode(DjangoObjectType):
    class Meta:
        model = Anime
        #3
        interfaces = (graphene.relay.Node, )


class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (graphene.relay.Node,)


class RelayQuery(graphene.ObjectType):
    #4
    relay_anime = graphene.relay.Node.Field(AnimeNode)
    #5
    relay_anime = DjangoFilterConnectionField(AnimeNode, filterset_class=AnimeFilter)

class RelayCreateAnime(graphene.relay.ClientIDMutation):
    anime= graphene.Field(AnimeNode)

    class Input:
        name = graphene.String()
        episode_count = graphene.Int()
        season_count = graphene.Int()
        status = graphene.String()
        description = graphene.String()
        studio = graphene.String()
    def mutate_and_get_payload(root, info, **input):
        user = info.context.user or None

        anime = Anime(
            name=input.get('name'),
            episode_count=input.get('episode_count'),
            season_count=input.get('season_count'),
            status=input.get('status'),
            description=input.get('description'),
            studio=input.get('studio'),
            posted_by=user,
        )
        anime.save()

        return RelayCreateAnime(anime=anime)


class RelayMutation(graphene.AbstractType):
    relay_create_anime = RelayCreateAnime.Field()