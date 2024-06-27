from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel  # Importation de Pydantic pour créer des modèles de données


app = FastAPI()


# création d'un modèle d'utilisateur avec Pydantic
class User(BaseModel):
    id: int
    name: str
    age: Union[int, None] = None

@app.get("/", description='Our main root')
def read_root():
    return {"Hi": "I'm fastAPI"}


@app.get("/users")
def users_list():
    return {"message" : "there are all users"}


@app.get("/users/me")
def current_user():
    return {"user id" : "this is the current user"}


"""@app.get("/users/{id}")
def users_info(id):
    return {"user id" : id}"""


@app.get("/users/{user_id}", description='Get user by ID')
def get_user(user_id: int):
    return {"user_id": user_id, "message": "Here is the user you requested"}


fake_items_db = [{"item_name" : "Foo"}, {"item_name" : "Bar"}, {"item_name" : "Baz"}]

@app.get("/items")
def list_items(skip : int = 0 , limit : int = 10):
    return fake_items_db[skip : skip+limit]

@app.get("/users/user/{name}")
def user_name (name):
    return {"user name : " :  name}

# création d'un utilisateur
@app.post("/users/", description='Création d\'un nouvel utilisateur')
def create_user(user: User):
    return {"message" : f"Utilisateur {user.name} créé avec succès", "user": user}


