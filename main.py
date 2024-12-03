from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List
from provenance import provenance

app = FastAPI()

# In-memory storage for simplicity
users = {}
posts = {}
comments = {}
likes = {}

# Models
class User(BaseModel):
    username: str
    password: str

class Post(BaseModel):
    title: str
    content: str
    author: str

class Comment(BaseModel):
    post_id: int
    content: str
    author: str

class Like(BaseModel):
    post_id: int
    user: str

# Dependency to simulate user authentication
def get_current_user(username: str = Query(...)):
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[username]

# Functions with provenance annotations
@app.post("/register")
@provenance()
def register(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[user.username] = user
    return {"message": "User registered successfully"}

@app.post("/login")
@provenance()
def login(user: User):
    if user.username not in users or users[user.username].password != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}

@app.post("/posts")
@provenance()
def create_post(post: Post, current_user: User = Depends(get_current_user)):
    post_id = len(posts) + 1
    posts[post_id] = post
    return {"message": "Post created successfully", "post_id": post_id}

@app.put("/posts/{post_id}")
@provenance()
def edit_post(post_id: int, post: Post, current_user: User = Depends(get_current_user)):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    posts[post_id] = post
    return {"message": "Post edited successfully"}

@app.post("/comments")
@provenance()
def create_comment(comment: Comment, current_user: User = Depends(get_current_user)):
    comment_id = len(comments) + 1
    comments[comment_id] = comment
    return {"message": "Comment created successfully", "comment_id": comment_id}

@app.put("/comments/{comment_id}")
@provenance()
def edit_comment(comment_id: int, comment: Comment, current_user: User = Depends(get_current_user)):
    if comment_id not in comments:
        raise HTTPException(status_code=404, detail="Comment not found")
    comments[comment_id] = comment
    return {"message": "Comment edited successfully"}

@app.post("/likes")
@provenance()
def like_post(like: Like, current_user: User = Depends(get_current_user)):
    like_id = len(likes) + 1
    likes[like_id] = like
    return {"message": "Post liked successfully", "like_id": like_id}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)