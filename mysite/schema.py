import graphene
# from graphene.types import field
from graphene_django import DjangoObjectType
from omok.models import Todo

class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        # field = ("id","text","isCompleted")

class Query(graphene.ObjectType):
    all_todolist = graphene.List(TodoType)
    def resolve_all_todolist(self, info):
        # We can easily optimize query count in the resolve method
        return Todo.objects.all()

    # category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))
    # def resolve_category_by_name(root, info, name):
    #     try:
    #         return Category.objects.get(name=name)
    #     except Category.DoesNotExist:
    #         return None

schema = graphene.Schema(query=Query)