import requests
import random
import string
from concurrent.futures import ThreadPoolExecutor
import logging

BASE_URL = "http://127.0.0.1:8000"

logging.basicConfig(level=logging.INFO)

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def register_user(username, password):
    response = requests.post(f"{BASE_URL}/register", json={"username": username, "password": password})
    logging.info(f"Register user {username}: {response.status_code}")
    return response.json()

def login_user(username, password):
    response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    logging.info(f"Login user {username}: {response.status_code}")
    return response.json()

def create_post(title, content, author):
    response = requests.post(f"{BASE_URL}/posts?username={author}", json={"title": title, "content": content, "author": author})
    logging.info(f"Create post by {author}: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to create post: {response.text}")
        return {}

def edit_post(post_id, title, content, author):
    response = requests.put(f"{BASE_URL}/posts/{post_id}?username={author}", json={"title": title, "content": content, "author": author})
    logging.info(f"Edit post {post_id} by {author}: {response.status_code}")
    return response.json()

def create_comment(post_id, content, author):
    response = requests.post(f"{BASE_URL}/comments?username={author}", json={"post_id": post_id, "content": content, "author": author})
    logging.info(f"Create comment on post {post_id} by {author}: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to create comment: {response.text}")
        return {}

def edit_comment(comment_id, post_id, content, author):
    response = requests.put(f"{BASE_URL}/comments/{comment_id}?username={author}", json={"post_id": post_id, "content": content, "author": author})
    logging.info(f"Edit comment {comment_id} on post {post_id} by {author}: {response.status_code}")
    return response.json()

def like_post(post_id, user):
    response = requests.post(f"{BASE_URL}/likes?username={user}", json={"post_id": post_id, "user": user})
    logging.info(f"Like post {post_id} by {user}: {response.status_code}")
    return response.json()

def simulate_interactions(num_users=100, num_posts=1000, num_comments=5000, num_likes=10000):
    users = [random_string() for _ in range(num_users)]
    posts = []
    comments = []

    # Register users
    for user in users:
        register_user(user, "password")

    # Create posts
    for _ in range(num_posts):
        author = random.choice(users)
        post = create_post(random_string(), random_string(50), author)
        if "post_id" in post:
            posts.append(post["post_id"])

    # Create comments
    for _ in range(num_comments):
        author = random.choice(users)
        if posts:
            post_id = random.choice(posts)
            comment = create_comment(post_id, random_string(50), author)
            if "comment_id" in comment:
                comments.append(comment["comment_id"])

    # Edit posts
    for post_id in posts:
        author = random.choice(users)
        edit_post(post_id, random_string(), random_string(50), author)

    # Edit comments
    for comment_id in comments:
        author = random.choice(users)
        if posts:
            post_id = random.choice(posts)
            edit_comment(comment_id, post_id, random_string(50), author)

    # Like posts
    for _ in range(num_likes):
        user = random.choice(users)
        if posts:
            post_id = random.choice(posts)
            like_post(post_id, user)

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(simulate_interactions) for _ in range(10)]
        for future in futures:
            future.result()