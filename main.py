import yaml

# from custom_provenance import provenance as p
import provenance as p
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Dict

import logging


import provenance as p
from functools import wraps


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load the YAML configuration file
with open("basic_config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Ensure the default_repo is set in the configuration
if "default_repo" not in config:
    raise ValueError("The 'default_repo' key is missing in the configuration")

# Pass the configuration dictionary to load_config
p.load_config(config)

app = FastAPI()

# In-memory storage for simplicity
users: Dict[str, "User"] = {}
posts: Dict[int, "Post"] = {}
comments: Dict[int, "Comment"] = {}
likes: Dict[int, List[str]] = {}


# Models
class User(BaseModel):
    username: str
    password: str


class Post(BaseModel):
    id: int
    title: str
    content: str
    author: str


class NewPost(BaseModel):
    title: str
    content: str
    author: str


class Comment(BaseModel):
    id: int
    post_id: int
    content: str
    author: str


class NewComment(BaseModel):
    post_id: int
    content: str
    author: str


class Like(BaseModel):
    post_id: int
    user: str


# Dependency to simulate user authentication
@p.provenance()
def get_current_user(username: str = Query(...)):
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")
    print("\n\nget_user\n" + users[username].username)
    return users[username]


@p.provenance()
def registT(username):
    return username


# User registration
@app.post("/register")
def register(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    aux = registT(user.username)
    users[aux] = user
    return {"message": "User registered successfully"}


@p.provenance()
def loginT(username):
    return username


# User login
@app.post("/login")
def login(user: User):
    if user.username not in users or users[user.username].password != user.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    aux = loginT(user.username)
    return users[aux]
    # return {"message": "Login successful"}


@p.provenance()
def createPostT(id, title, author):
    return id


# Create a post
@app.post("/posts")
def create_post(post: NewPost, current_user: User = Depends(get_current_user)):
    new_id = len(posts) + 1
    new_post = Post(
        id=new_id, title=post.title, content=post.content, author=post.author
    )
    aux = createPostT(new_post.id, new_post.title, new_post.author)
    posts[new_id] = new_post
    return new_post


@p.provenance()
def editPostT(id, title, author):
    return id


# Edit a post
@app.put("/posts/{post_id}")
def edit_post(post_id: int, post: Post, current_user: User = Depends(get_current_user)):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    if posts[post_id].author != current_user.username:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")
    editPostT(post.id, post.title, post.author)
    posts[post_id] = post
    return post


@p.provenance()
def createCommentT(id, content, author):
    return id


# Create a comment
@app.post("/comments")
def create_comment(comment: NewComment, current_user: User = Depends(get_current_user)):
    new_id = len(comments) + 1
    new_comment = Comment(
        id=new_id,
        post_id=comment.post_id,
        content=comment.content,
        author=comment.author,
    )
    createCommentT(new_comment.id, new_comment.content, new_comment.author)
    comments[new_id] = new_comment
    return new_comment


@p.provenance()
def editCommentT(id, content, author):
    return id


# Edit a comment
@app.put("/comments/{comment_id}")
@p.provenance()
def edit_comment(
    comment_id: int, comment: Comment, current_user: User = Depends(get_current_user)
):
    if comment_id not in comments:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comments[comment_id].author != current_user.username:
        raise HTTPException(
            status_code=403, detail="Not authorized to edit this comment"
        )
    editCommentT(comment.id, comment.content, comment.author)
    comments[comment_id] = comment
    return comment


@p.provenance()
def deleteCommentT(id):
    return id


# Delete a comment
@app.delete("/comments/{comment_id}")
@p.provenance()
def delete_comment(comment_id: int, current_user: User = Depends(get_current_user)):
    if comment_id not in comments:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comments[comment_id].author != current_user.username:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this comment"
        )
    deleteCommentT(comment_id)
    del comments[comment_id]
    return {"message": "Comment deleted successfully"}


# Like a post
@app.post("/posts/{post_id}/like")
def like_post(post_id: int, current_user: User = Depends(get_current_user)):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    if post_id not in likes:
        likes[post_id] = []
    if current_user.username in likes[post_id]:
        raise HTTPException(status_code=400, detail="Post already liked")

    likes[post_id].append(current_user.username)
    return {"message": "Post liked successfully"}


# Like a comment
@app.post("/comments/{comment_id}/like")
@p.provenance()
def like_comment(comment_id: int, current_user: User = Depends(get_current_user)):
    if comment_id not in comments:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment_id not in likes:
        likes[comment_id] = []
    if current_user.username in likes[comment_id]:
        raise HTTPException(status_code=400, detail="Comment already liked")
    likes[comment_id].append(current_user.username)
    return {"message": "Comment liked successfully"}
