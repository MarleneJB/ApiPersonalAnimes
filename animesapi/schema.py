import graphene
import graphql_jwt
import animes.schema
import users.schema
import animes.schema_relay

class Query(
    users.schema.Query,
    animes.schema.Query,
    animes.schema_relay.RelayQuery,
    graphene.ObjectType,
):
    pass

class Mutation(
    users.schema.Mutation,
    animes.schema.Mutation,
    animes.schema_relay.RelayMutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)