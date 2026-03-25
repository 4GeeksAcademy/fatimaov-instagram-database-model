from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255),nullable=False)
    posts: Mapped[list["Post"]] = relationship(back_populates = "creator")
    comments: Mapped[list["Comment"]] = relationship(back_populates = "creator")
    likes: Mapped[list["Like"]] = relationship(back_populates = "user")


    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "posts": [post.serialize() for post in self.posts],
            "comments": [comment.serialize() for comment in self.comments],
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    caption: Mapped[str] = mapped_column(String(150), unique = False, nullable = True)
    media_url: Mapped[str] = mapped_column(String(255), unique = False, nullable = False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    creator: Mapped["User"] = relationship(back_populates = "posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates = "post")
    likes: Mapped[list["Like"]] = relationship(back_populates = "post")

    def serialize(self):
        return {
            "id": self.id,
            "caption": self.caption,
            "media_url": self.media_url,
            "creator_id": self.creator_id,
            "comments": [comment.serialize() for comment in self.comments],
        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    content: Mapped[str] = mapped_column(String(500), nullable = False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates = "comments")
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    creator: Mapped["User"] = relationship(back_populates = "comments")

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "post_id": self.post_id,
            "creator_id": self.creator_id,
        }

class Like(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates = "likes")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates = "likes")

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
        }
