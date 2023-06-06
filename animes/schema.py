import graphene
from graphene_django import DjangoObjectType
from .models import Anime
from users.schema import UserType
from animes.models import Anime, Vote
from graphql import GraphQLError
from django.db.models import Q


class AnimeType(DjangoObjectType):
    class Meta:
        model = Anime

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

    
class CreateAnime(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    episode_count = graphene.Int()
    season_count = graphene.Int()
    status = graphene.String()
    description = graphene.String()
    studio = graphene.String()
    posted_by = graphene.Field(UserType)

    #2
    class Arguments:
        name = graphene.String()
        episode_count = graphene.Int()
        season_count = graphene.Int()
        status = graphene.String()
        description = graphene.String()
        studio = graphene.String()
    #3
    def mutate(self, info, name, episode_count, season_count, status,studio, description=None):
    
        user = info.context.user or None

        anime = Anime(name=name, episode_count=episode_count,season_count=season_count,status=status, description=description or "", studio=studio,
        posted_by=user,              )
        anime.save()

        return CreateAnime(
            id=anime.id,
            name=anime.name,
            episode_count=anime.episode_count,
            season_count=anime.season_count,
            status=anime.status,
            description=anime.description,
            studio=anime.studio,
            posted_by=anime.posted_by,
        )


#4
class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    character = graphene.Field(AnimeType)

    class Arguments:
        anime_id = graphene.Int()

    def mutate(self, info, anime_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        anime = Anime.objects.filter(id=anime_id).first()
        if not anime:
            raise Exception('Invalid Anime!')

        Vote.objects.create(
            user=user,
            anime=anime,
        )

        return CreateVote(user=user, anime=anime)

class Query(graphene.ObjectType):
    animes = graphene.List(
        AnimeType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    votes = graphene.List(VoteType)

    def resolve_animes(self, info, search=None, first=None, skip=None, **kwargs):
        qs = Anime.objects.all()

        if search:
            filter = (
                Q(name__icontains=search) |
                Q(episode_count__icontains=search) |
                Q(season_count__icontains=search) |
                Q(status__icontains=search) |
                Q(description__icontains=search) |
                Q(studio__icontains=search)
                
            )
            qs = qs.filter(filter)
        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

class Mutation(graphene.ObjectType):
    create_anime = CreateAnime.Field()
    create_vote = CreateVote.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
