import pytest
from .test_schema import schema

@pytest.mark.django_db
def test_query_should_return_user():
    query = """
        query {
            user(id:"1") {
                id
                name
            }
        }
    """
    result = schema.execute(query, context_value = {"headers": {'authorization':'kk57vea3ara1kjkn8462mah4vgjdx35z'}})
    assert not result.errors
    assert result.user is {'id': 1, 'name': 'DimCigarette'}


# def test_query_should_raise_error():
#     with pytest.raises(Exception):

#         query = """
#         query {
#             user(id:"1") {
#                 id
#                 name
#             }
#         }
#         """
#         result = schema.execute(query, context_value = {"headers": {'authorization':'aa'}})
#         assert result.errors


# def test_sign_in_guest():
#     query = """py
#         mutation {
#             signInGuest {
#                 id
#                 name
#                 sid
#             }
#         }
#     """
#     result = schema.execute(query, context_value = {"headers": {'authorization':''}})
#     assert not result.errors


