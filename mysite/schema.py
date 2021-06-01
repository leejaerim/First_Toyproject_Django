import graphene
from graphene.types.argument import Argument
# from graphene.types import field
from graphene_django import DjangoObjectType
from omok.models import Todo

class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        # field = ("id","text","isCompleted")

class Query(graphene.ObjectType):
    todos = graphene.List(TodoType)
    todo = graphene.Field(TodoType, id = graphene.ID())
    def resolve_todos(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Todo.objects.all()
    def resolve_todo(self, info , id ):
        return Todo.objects.get(pk = id)

class CreateTodo(graphene.Mutation):
    class Arguments:
        text = graphene.String()
        isCompleted = graphene.Int()
    todo = graphene.Field(TodoType)
    def mutate(self, info,text,isCompleted):
        todo = Todo.objects.create(
            text = text,
            isCompleted = isCompleted
        )
        todo.save()
        return CreateTodo(
        todo = todo 
        )
class UpdateTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        text = graphene.String()
        isCompleted = graphene.Int()
    todo = graphene.Field(TodoType)
    def mutate(self, info, id, text = None, isCompleted=None):
        todo = Todo.objects.get(pk=id)
        todo.text = text if text is not None else todo.text
        todo.isCompleted = isCompleted if isCompleted is not None else todo.isCompleted
        todo.save()
        return UpdateTodo(
            todo=todo
        )
class DeleteTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    todo = graphene.Field(TodoType)
    def mutate(self,info , id):
        todo = Todo.objects.get(pk=id)
        if todo is not None:
            todo.delete()
        return DeleteTodo(todo=todo)
class Mutation(graphene.ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()

schema = graphene.Schema(query=Query, mutation= Mutation)