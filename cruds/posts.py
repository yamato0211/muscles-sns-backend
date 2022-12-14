from typing import List
from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from schemas.posts import Post as PostSchema
from db.models import Post

def create_post_by_user_id(db: Session, content: str, user_id: str) -> PostSchema:
    # user_orm = db.query(User).filter(User.user_id == user_id).first()
    # if user_orm is None:
    #     raise HTTPException(status_code=404, detail='user not found')
    post_orm = Post(
        content=content,
        user_id=user_id,
    )
    db.add(post_orm)
    db.commit()
    db.refresh(post_orm)
    post = PostSchema.from_orm(post_orm)
    return post

def get_timeline(db: Session) -> List[PostSchema]:
    posts_orm = db.query(Post).all()
    posts = list(map(PostSchema.from_orm,posts_orm))
    return posts

def get_post_detail_by_post_id(db: Session, post_id: str) -> PostSchema:
    post_orm = db.query(Post).filter(Post.post_id == post_id).first()
    if post_orm is None:
        raise HTTPException(status_code=404, detail="post not found")
    post = PostSchema.from_orm(post_orm)
    return post

def get_posts_by_user_id(db: Session, user_id: str) -> List[PostSchema]:
    posts_orm = db.query(Post).filter(Post.user_id == user_id).all()
    posts = list(map(PostSchema.from_orm, posts_orm))
    return posts

def delete_post_by_post_id(db: Session, post_id: str, user_id: str) -> None:
    post = db.query(Post).filter(Post.post_id == post_id, Post.user_id == user_id).first()
    if post is None:
        raise HTTPException(status_code=400, detail="post not deleted")
    db.delete(post)
    db.commit()
    return