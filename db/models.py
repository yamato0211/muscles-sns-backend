from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4

Base = declarative_base()

def create_uuid():
    return str(uuid4())


class PostFavorites(Base):
    __tablename__ = "post_favorites"
    user_id = Column(String, ForeignKey("users.user_id"), primary_key=True)
    post_id = Column(String, ForeignKey("posts.post_id"), primary_key=True)

class CommentFavorites(Base):
    __tablename__ = "comment_favorites"
    user_id = Column(String, ForeignKey("users.user_id"), primary_key=True)
    comment_id = Column(String, ForeignKey("comments.comment_id"), primary_key=True)

class User(Base):
    __tablename__ = "users"
    user_id = Column(String,primary_key=True, default=create_uuid)
    name = Column(String)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=True)


class Post(Base):
    __tablename__ = "posts"
    post_id = Column(String, primary_key=True, default=create_uuid)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    user_id = Column(String, ForeignKey("users.user_id"))
    user = relationship("User")
    favorites = relationship("User", secondary=PostFavorites.__tablename__)
    comments = relationship("Comment")


class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(String, primary_key=True, default=create_uuid)
    user_id = Column(String, ForeignKey("users.user_id"))
    post_id = Column(String, ForeignKey("posts.post_id"))
    content = Column(String)
    user = relationship("User")
    favorites = relationship("User", secondary=CommentFavorites.__tablename__)
