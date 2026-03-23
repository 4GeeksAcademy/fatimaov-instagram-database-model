from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, ForeignKey

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(20),nullable=False)
    posts: Mapped[list["Post"]] = relationship(back_populates = "creator")


    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "posts": [post.serialize() for post in self.posts],
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    caption: Mapped[str] = mapped_column(String(150), unique = False, nullable = True)
    media_url: Mapped[str] = mapped_column(String(), unique = False, nullable = False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    creator : Mapped["User"] = relationship(back_populates = "posts")

    def serialize(self):
        return {
            "id": self.id,
            "caption": self.caption,
            "media_url": self.media_url,
            "creator_id": self.creator_id,
        }
