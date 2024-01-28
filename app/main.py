
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


# print(f"DB Password:  {settings.database_password}")
# print(f"DB Username:  {settings.database_username}")

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = ["https://www.google.com", "https://www.youtube.com"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router) 
app.include_router(auth.router)
app.include_router(vote.router)   
       

# my_posts = [
#     {
#         "title": "title of post 1",
#         "content": "content of post 1",
#         "id": 1
#     },
#     {
#         "title": "title of post 2",
#         "content": "content of post 2",
#         "id": 2
#     }
#     ]    

@app.get("/") # decorator
def root():
    return {"message": "Hello Explorers, welcome to amazing word of APIs, serving from cloud ubuntu"}

# # @app.get("/sqlalchemy")
# # def test_post(db: Session = Depends(get_db)):

# #     posts = db.query(models.Post).all()
# #     return{"data": posts}


# def find_post(id):
#     for post in my_posts:
#         if post["id"] == id:
#             return post
        

            

# @app.get("/posts/latest")
# def get_post():
#     post = my_posts[-1]
#     return {"post_details": post}   

# def find_index_post(id):
#     for index, post in enumerate(my_posts):
#         if post["id"] == id:
#             return index
        
       