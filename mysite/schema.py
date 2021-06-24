import graphene
from todolist.schema import TodoMutation, TodoQuery
from omok.schema import OmokMutation, OmokQuery
from toy_auth.schema import UserMutation, UserQuery


class Query(
    UserQuery,
    TodoQuery,
    OmokQuery,
    graphene.ObjectType
): pass
    

class Mutation(
    UserMutation,
    TodoMutation,
    OmokMutation,
    graphene.ObjectType
): pass
    

schema = graphene.Schema(query=Query, mutation=Mutation)
