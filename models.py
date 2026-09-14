from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)
    
    # Relationship: Allows us to do user.posts to see all their posts
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    
    # Link: The 'user_id' column stores the ID of the user who wrote the post
    # ondelete="CASCADE" means: if the user is deleted, delete their posts too.
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    
    # Python helpers
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String(500))
    
    # Links: One link to the post, one link to the user who wrote it
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    
    # Python helpers
    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")