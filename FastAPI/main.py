from typing import Union, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  # Importation de Pydantic pour créer des modèles de données


app = FastAPI()


# création d'un modèle d'utilisateur avec Pydantic
class User(BaseModel):
    id: int
    name: str
    age: Union[int, None] = None

# liste pour stocker les utilisateurs
users_db: List[User] = []

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

# obtenir un utilisateur donné par son ID
@app.get("/users/{user_id}", description='Get user by ID')
def get_user(user_id: int):
    for user in users_db:
        if(user.id == user_id):
            return {"user_id": user_id, "message": "Voici l'utilisateur que vous avez demandé", "user" :user}
    raise HTTPException(status_code=404, detail= "Utilisateur non trouvé")


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
    #Vérifier si un utilisateur existait déjà avec ce même id
    for existing_user in users_db:
        if existing_user.id == user.id:
            raise HTTPException(status_code=404, detail= f'Utilisateur avec cet id ({user.id}) existe déjà')
    users_db.append(user)
    print(users_db)
    return {"message" : f"Utilisateur {user.name} créé avec succès", "user": user}

# mise à jour d'un utilisateur
@app.put("/users/{user_id}", description='Mise à jour d\'un utilisateur')
def update_user(user_id: int, user: User):
    for index, existing_user in enumerate(users_db):
        if existing_user.id == user_id:
            users_db[index] = user
            return{"message": f"Utilisateur {user.name} mise à jour avec succès"}
    print(users_db)
    raise HTTPException(status_code=404, detail= f'Utilisateur avec l\'id ({user.id}) n\'existe pas')

# suppression d'un utilisateur
@app.delete("/users/{user_id}", description='Suppression d\'un utilisateur')
def delete_user(user_id: int):
    for index, existing_user in enumerate(users_db):
        if(existing_user.id == user_id):
            users_db.pop(index)
            return{"message" : f"Utilisateur avec l'ide {user_id} supprimé avec succès"}
    print(users_db)
    raise HTTPException(status_code=404, detail=f'Utilisateur non trouvé')
