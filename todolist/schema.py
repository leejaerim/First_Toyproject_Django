import graphene
from graphene_django import DjangoObjectType
from .models import Todo


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        field = ("id", "text", "isCompleted")


class CreateTodo(graphene.Mutation):
    class Arguments:
        text = graphene.String()
        isCompleted = graphene.Boolean(required=False)

    id = graphene.ID()
    text = graphene.String()
    isCompleted = graphene.Boolean()

    def mutate(self, info, text, isCompleted=None):
        _isCompleted = None
        if isCompleted is not None:
            if isCompleted:
                _isCompleted = 1
            else :
                _isCompleted = 0
        todo = Todo.objects.create(text=text, isCompleted=_isCompleted)
        todo.save()
        return CreateTodo(id=todo.id, text= text, isCompleted=isCompleted)


class UpdateTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        text = graphene.String()
        isCompleted = graphene.Boolean()

    id = graphene.ID()
    text = graphene.String()
    isCompleted = graphene.Boolean()

    def mutate(self, info, id, text=None, isCompleted=None):
        _isCompleted = None
        if isCompleted is not None:
            if isCompleted:
                _isCompleted = 1
            else :
                _isCompleted = 0
        
        todo = Todo.objects.get(pk=id)
        todo.text = text if text is not None else todo.text
        todo.isCompleted = _isCompleted
        todo.save()
        return UpdateTodo(id=id, text = text, isCompleted=isCompleted)


class DeleteTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    id = graphene.ID()

    def mutate(self, info, id):
        todo = Todo.objects.get(pk=id)
        if todo is not None:
            todo.delete()
        return DeleteTodo(id=id)
