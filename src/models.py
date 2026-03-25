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

    # Relationship One - Many
    posts: Mapped[list["Post"]] = relationship("Post", back_populates = "user")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates = "user")
    likes: Mapped[list["Like"]] = relationship("Like", back_populates = "user")
    # Relationship Many - Many
    followings: Mapped[list["Follows"]] = relationship("Follows",
        foreign_keys="Follows.follower_id",
        back_populates="follower"
    )
    followers: Mapped[list["Follows"]] = relationship(
        "Follows",
        foreign_keys="Follows.followed_id",
        back_populates="followed"
    )


    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "posts": [post.serialize() for post in self.posts],
            "comments": [comment.serialize() for comment in self.comments],
            "followings": [following.serialize() for following in self.followings],
            "followwers": [follower.serialize() for follower in self.followers],
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    caption: Mapped[str] = mapped_column(String(150), unique = False, nullable = True)
    media_url: Mapped[str] = mapped_column(String(255), unique = False, nullable = False)
    # ForeignKey
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # Relationship Many - One
    user: Mapped["User"] = relationship("User", back_populates = "posts")
    # Relationship One - Many
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates = "post")
    likes: Mapped[list["Like"]] = relationship("Like", back_populates = "post")

    def serialize(self):
        return {
            "id": self.id,
            "caption": self.caption,
            "media_url": self.media_url,
            "user_id": self.creator_id,
            "user": self.creator,
            "comments": [comment.serialize() for comment in self.comments],
        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    content: Mapped[str] = mapped_column(String(500), nullable = False)
    # ForeignKeys
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # Relationship Many - One
    user: Mapped["User"] = relationship("User", back_populates = "comments")
    post: Mapped["Post"] = relationship("Post", back_populates = "comments")

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "post_id": self.post_id,
            "creator_id": self.creator_id,
            "post": self.post,
            "user": self.user,
        }

class Like(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    # ForeignKeys
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # Relationship Many - One
    post: Mapped["Post"] = relationship("Post", back_populates = "likes")
    user: Mapped["User"] = relationship("User", back_populates = "likes")

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
        }
    
class Follows(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    # ForeignKeys
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    followed_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # Relationship Many - Many
    follower: Mapped["User"] = relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="followings"
    )
    followed: Mapped["User"] = relationship(
        "User",
        foreign_keys=[followed_id],
        back_populates="followers"
    )
