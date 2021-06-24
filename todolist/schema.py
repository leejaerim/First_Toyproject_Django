from todolist.types import TodoType
from toy_auth.middleware import checkToken
import graphene
from .models import Todo
from toy_auth.models import User


class TodoQuery(graphene.ObjectType):
    todos = graphene.List(TodoType)
    
    @checkToken
    def resolve_todos(self, info, **kwargs):
        return Todo.objects.filter(user_id = info.context.uid).all()

class CreateTodo(graphene.Mutation):
    class Arguments:
        text = graphene.String()
        isCompleted = graphene.Boolean(required=False)

    id = graphene.ID()
    text = graphene.String()
    isCompleted = graphene.Boolean()

    @checkToken
    def mutate(self, info, text, isCompleted=None):
        user = User.objects.get(id=info.context.uid)
        _isCompleted = None
        if isCompleted is not None:
            if isCompleted:
                _isCompleted = 1
            else:
                _isCompleted = 0
        todo = Todo.objects.create(text=text,
                                    isCompleted=_isCompleted,
                                    user=user)
        return CreateTodo(id=todo.id, text=text, isCompleted=isCompleted)
     


class UpdateTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        text = graphene.String()
        isCompleted = graphene.Boolean()

    id = graphene.ID()
    text = graphene.String()
    isCompleted = graphene.Boolean()

    @checkToken
    def mutate(self, info, id, text=None, isCompleted=None):
        try :
            todo = Todo.objects.get(pk=id)
            if todo.user.id is info.context.uid:
                _isCompleted = None
                if isCompleted is not None:
                    if isCompleted:
                        _isCompleted = 1
                    else:
                        _isCompleted = 0

                todo.text = text if text is not None else todo.text
                todo.isCompleted = _isCompleted
                todo.save()
                return UpdateTodo(id=id, text=text, isCompleted=isCompleted)
        except Todo.DoesNotExist:
            raise Exception('Inavlid Todo Object')


class DeleteTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    id = graphene.ID()

    def mutate(self, info, id):
        try:
            todo = Todo.objects.get(pk=id)
            if todo.user.id is info.context.uid:
                todo.delete()
                return DeleteTodo(id=id)
        except Todo.DoesNotExist:
            raise Exception('Invalid Todo Object')


class TodoMutation(graphene.ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()
