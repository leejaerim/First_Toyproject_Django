from todolist.models import Todo
from toy_auth.models import GuestUser
from django.test.client import RequestFactory
from mysite.schema import schema
from graphene.test import Client
from django.test import TestCase
from toy_auth.middleware import passTokenTest


class TestUserSchema(TestCase):
    def setUp(self):
        self.client = Client(schema, middleware=[passTokenTest])
        self.request = RequestFactory().get('/')
        self.user = GuestUser.objects.signIn(token='')
        self.uid = self.user.id
        self.todoId = Todo.objects.create(text='xx', user = self.user).pk

    def test_create_todo(self):
        self.request.headers = {'authorization': ''}
        self.request.uid = self.uid

        query = """
            mutation ($text:String, $isCompleted:Boolean)
            {
                createTodo(text:$text, isCompleted:$isCompleted) {
                    id
                    text
                }
            }
        """
        response = self.client.execute(
            query,
            variables = {'text': 'I am testing'},
            context_value = self.request
        )

        assert 'errors' not in response
        assert response.get('data').get('createTodo').get('text') == 'I am testing' 
    
    def test_update_todo(self):
        self.request.headers = {'authorization': ''}
        self.request.uid = self.uid

        query = """
            mutation ($id:ID, $text:String, $isCompleted:Boolean)
            {
                updateTodo(id:$id, text:$text, isCompleted:$isCompleted) {
                    id
                    text
                }
            }
        """
        response = self.client.execute(
            query,
            variables = {'id': self.todoId, 'text': 'I am testing'},
            context_value = self.request
        )

        assert 'errors' not in response
        assert response.get('data').get('updateTodo').get('text') == 'I am testing' 


    def test_query_todo(self):
        self.request.headers = {'authorization': ''}
        self.request.uid = self.uid

        query = """
            query 
            {
                todos {
                    id
                    text
                }
            }
        """
        response = self.client.execute(
            query,
            context_value = self.request
        )

        assert 'errors' not in response
        assert response.get('data').get('todos') is not None 

    def test_delete_todo(self):
        self.request.headers = {'authorization': ''}
        self.request.uid = self.uid

        query = """
            mutation ($id:ID)
            {
                deleteTodo(id:$id) {
                    id
                }
            }
        """
        response = self.client.execute(
            query,
            variables = {'id': self.todoId},
            context_value = self.request
        )

        assert 'errors' not in response
        assert response.get('data').get('deleteTodo').get('id') == str(self.todoId)