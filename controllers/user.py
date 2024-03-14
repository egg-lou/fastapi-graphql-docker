from fastapi import APIRouter
import strawberry
from type.user import Query, Mutation
from strawberry.asgi import GraphQL

user = APIRouter()
schema = strawberry.Schema(query=Query, mutation=Mutation)
grapql_app = GraphQL(schema)
user.add_route('/graphql', grapql_app)