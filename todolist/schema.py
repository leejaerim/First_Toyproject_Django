import graphene
from .models import Todo
from toy_auth.models import User
from toy_auth.types import UserInput


class CreateTodo(graphene.Mutation):
    class Arguments:
        text = graphene.String()
        isCompleted = graphene.Boolean(required=False)
        user = graphene.Argument(UserInput)

    id = graphene.ID()
    text = graphene.String()
    isCompleted = graphene.Boolean()

    def mutate(self, info, text, user, isCompleted=None):
        try:
            user = User.objects.get(id=user.id)
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
        except User.DoesNotExist:
            raise Exception('Unauthenticated Access')


class UpdateTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        text = graphene.String()
        isCompleted = graphene.Boolean()
        user = graphene.Argument(UserInput)

    id = graphene.ID()
    text = graphene.String()
    isCompleted = graphene.Boolean()

    def mutate(self, info, id, user, text=None, isCompleted=None):
        try:
            todo = Todo.objects.get(pk=id)
            if todo.user.id is int(user.id):
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
            else:
                raise Exception('Unauthenticated User Access')

        except Todo.DoesNotExist:
            raise Exception('Invalid Todo Object')


class DeleteTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        user = graphene.Argument(UserInput)

    id = graphene.ID()

    def mutate(self, info, id, user):
        try:
            todo = Todo.objects.get(pk=id)
            if todo.user.id is int(user.id):
                todo.delete()
                return DeleteTodo(id=id)
            else:
                raise Exception('Unauthenticated User Access')

        except Todo.DoesNotExist:
            raise Exception('Invalid Todo Object')
