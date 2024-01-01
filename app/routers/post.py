from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix= "/posts",
    tags= ['Posts']
)





# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int=10, skip: int=0, search: Optional[str] = ""):
    # cur.execute("""SELECT * FROM public.posts""")
    # posts = cur.fetchall()
    # print(limit)
  
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    # return {"data": posts}
    return posts
    # return results

""" @router.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title: {payload['title']} content: {payload['content']}"} """


@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    # post_dict = post.dict()
    # post_dict["id"] = randrange(0, 10000000)
    # my_posts.routerend(post_dict)
    # cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #             (post.title, post.content,post.published))
    # new_post = cur.fetchone()
    # conn.commit()
    print(current_user.id)
    
    # print(current_user.email)
    print(post.model_dump())
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(user_id)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # return {"data": new_post}
    return new_post
    

         

@router.get("/{id}", response_model=schemas.PostOut)
#def get_post(id : int, response: Response):
def get_post(id : int, db: Session=Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cur.execute("""SELECT * FROM posts where id = %s """,(str(id),))
    # post = cur.fetchone()
    #post = find_post(id)
    # post = db.query(models.Post).filter(models.Post.id==id).first()

    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    # print(post)
    if not post:    
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id={id} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
        
    # return {"post_details": post}
    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    # delete_post = cur.fetchone()
    # conn.commit()
    #index = find_index_post(id)
    #print(index)
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
    #if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authrorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()    
    #my_posts.pop(index)
    # post = find_post(id)
    # if not post:
    #     raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
    #                         detail= f"post with id: {id} does not exist")
    # my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("""UPDATE posts set title = %s, content = %s, published =%s WHERE id = %s RETURNING *""",
    #             (post.title, post.content, post.published, str(id),))
    # updated_post = cur.fetchone()
    # conn.commit()

    # print(updated_post)
    #index = find_index_post(id)
    #print(index)
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
    #if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_posts[index] = post_dict
    # post_query.update({'title': 'this is my updated tile', 'content':'This is my upated content'}, 
    # synchronize_session=False)

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authrorized to perform requested action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    # return {"data": post_query.first()}
    return post_query.first()