from typing import Union, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  # Importation de Pydantic pour créer des modèles de données
from sqlalchemy import Column, Integer, String, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

DATABASE_URL = "sqlite:///./test.db"

database = Database(DATABASE_URL)
metadata = MetaData()

Base = declarative_base()

# Modèle SQLAlchemy
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer, index=True)

# Création de la base de données et des tables
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Session de base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



app = FastAPI()


# création d'un modèle d'utilisateur avec Pydantic
class User(BaseModel):
    id: int
    name: str
    age: Union[int, None] = None

# liste pour stocker les utilisateurs
users_db: List[User] = []

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/", description='Our main root')
def read_root():
    return {"Hi": "I'm fastAPI"}


"""@app.get("/users")
def users_list():
    return {"message" : "there are all users"}"""

@app.get("/users", response_model=List[User])
async def users_list():
    query = UserModel.__table__.select()
    return await database.fetch_all(query)


@app.get("/users/me")
def current_user():
    return {"user id" : "this is the current user"}


"""@app.get("/users/{id}")
def users_info(id):
    return {"user id" : id}"""

# obtenir un utilisateur donné par son ID
@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    query = UserModel.__table__.select().where(UserModel.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


fake_items_db = [{"item_name" : "Foo"}, {"item_name" : "Bar"}, {"item_name" : "Baz"}]

@app.get("/items")
def list_items(skip : int = 0 , limit : int = 10):
    return fake_items_db[skip : skip+limit]

@app.get("/users/user/{name}")
def user_name (name):
    return {"user name : " :  name}


# création d'un utilisateur
@app.post("/users/", response_model=User)
async def create_user(user: User):
    query = UserModel.__table__.insert().values(id=user.id, name=user.name, age=user.age)
    await database.execute(query)
    return user


# mise à jour d'un utilisateur
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    query = UserModel.__table__.update().where(UserModel.id == user_id).values(name=user.name, age=user.age)
    await database.execute(query)
    return user


# suppression d'un utilisateur
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = UserModel.__table__.delete().where(UserModel.id == user_id)
    await database.execute(query)
    return {"message": f"Utilisateur avec l'ID {user_id} supprimé avec succès"}