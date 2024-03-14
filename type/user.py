import strawberry
import typing
from models.index import users
from conn.db import conn
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)


@strawberry.type
class User:
    id: int
    name: str
    email: str
    password: str


@strawberry.type
class Query:
    @strawberry.field
    def user(self, info, id: int) -> typing.Optional[User]:
        user = conn.execute(users.select().where(users.c.id == id)).fetchone()
        return user if user else None

    @strawberry.field
    def users(self, info) -> typing.List[User]:
        return conn.execute(users.select()).fetchall()


@strawberry.type
class Mutation:
    @strawberry.field
    def create_user(
        self, info, name: str, email: str, password: str
    ) -> typing.Optional[User]:
        hashed_password = cipher_suite.encrypt(password.encode()).decode()
        conn.execute(
            users.insert().values(name=name, email=email, password=hashed_password)
        )
        user = conn.execute(users.select().where(users.c.email == email)).fetchone()
        return user if user else None

    @strawberry.field
    def update_user(
        self, info, id: int, name: str, email: str, password: str
    ) -> typing.Optional[User]:
        hashed_password = cipher_suite.encrypt(password.encode()).decode()
        conn.execute(
            users.update()
            .values(name=name, email=email, password=hashed_password)
            .where(users.c.id == id)
        )
        user = conn.execute(users.select().where(users.c.id == id)).fetchone()
        return user if user else None

    @strawberry.field
    def delete_user(self, info, id: int) -> str:
        user = conn.execute(users.select().where(users.c.id == id)).fetchone()
        if user:
            conn.execute(users.delete().where(users.c.id == id))
            return "User deleted successfully."
        else:
            return "User not found."
