from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey
from typing import List

db = SQLAlchemy()

class Follower(db.Model):
    

    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    follower: Mapped["User"] = relationship( foreign_keys=[user_from_id], back_populates="following")
    followed: Mapped["User"] = relationship( foreign_keys=[user_to_id], back_populates="followers")


class User(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(nullable= False)
    firstname : Mapped[str] = mapped_column(String(120), nullable = False)
    lastname: Mapped[str] = mapped_column(String(120),nullable = False)
    email: Mapped[str] = mapped_column(String(120),nullable= False)
    password: Mapped[str] = mapped_column(String(120),nullable= False)

    posts: Mapped[List["Post"]] = relationship(back_populates="author")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")
    followers: Mapped[List["Follower"]] = relationship( foreign_keys=[Follower.user_to_id], back_populates="followed")
    following: Mapped[List["Follower"]] = relationship( foreign_keys=[Follower.user_from_id], back_populates="follower")

    def serialize(self):
        return {
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname":self.lastname
        
            # do not serialize the password, its a security breach
        }
    
class Comment(db.Model):
    id:Mapped[int] = mapped_column(primary_key = True)
    comment_text:Mapped[str] = mapped_column(String(120), nullable = False)
    user_id: Mapped[int] =mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    author: Mapped["User"] = relationship( back_populates="comments")
    post: Mapped["Post"] = relationship( back_populates="comments")

   

    def serialize(self):
        return{
            "comment_text": self.comment_text,
            "user_id":self.user_id,
            "post_id":self.post_id
        }

class Post(db.Model):
   id:Mapped[int] = mapped_column(primary_key = True)
   user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))

   author: Mapped["User"] = relationship(back_populates="posts")
   comments: Mapped[List["Comment"]] = relationship(back_populates="post")
   media_items: Mapped[List["Media"]] = relationship( back_populates="post")
   
   


class Media(db.Model):
    id:Mapped[int] = mapped_column(primary_key = True)
    type:Mapped[str] = mapped_column(String(120),nullable= False)
    url:Mapped[str]= mapped_column(String(400), nullable=False)
    post_id:Mapped[int]= mapped_column(ForeignKey("post.id"))


    post: Mapped["Post"] = relationship("Post", back_populates="media_items")






    



    

