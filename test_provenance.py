import requests
import threading
import random
import time

BASE_URL = "http://127.0.0.1:8000"

def register_user(username, password):
    response = requests.post(f"{BASE_URL}/register", json={"username": username, "password": password})
    print(response.json())

def login_user(username, password):
    response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    print(response.json())

def create_post(username, title, content):
    response = requests.post(f"{BASE_URL}/posts", json={"title": title, "content": content, "author": username}, params={"username": username})
    print(response.json())
    return response.json().get("id")

def edit_post(username, post_id, title, content):
    response = requests.put(f"{BASE_URL}/posts/{post_id}", json={"id": post_id, "title": title, "content": content, "author": username}, params={"username": username})
    print(response.json())

def create_comment(username, post_id, content):
    response = requests.post(f"{BASE_URL}/comments", json={"post_id": post_id, "content": content, "author": username}, params={"username": username})
    print(response.json())
    return response.json().get("id")

def like_post(username, post_id):
    response = requests.post(f"{BASE_URL}/posts/{post_id}/like", params={"username": username})
    print(response.json())

def like_comment(username, comment_id):
    response = requests.post(f"{BASE_URL}/comments/{comment_id}/like", params={"username": username})
    print(response.json())

def test_endpoints():
    # Register users
    for i in range(50):
        threading.Thread(target=register_user, args=(f"user{i}", "password")).start()
        time.sleep(0.1)  # Slight delay to avoid race conditions

    # Login users
    for i in range(50):
        threading.Thread(target=login_user, args=(f"user{i}", "password")).start()
        time.sleep(0.1)

    # Create posts
    post_ids = []
    for i in range(50):
        num_posts = random.randint(0, 5)  # Each user can create between 0 to 5 posts
        for _ in range(num_posts):
            post_id = create_post(f"user{i}", f"Title {i}", f"Content {i}")
            post_ids.append((post_id, f"user{i}"))
            time.sleep(0.1)

    # Edit posts
    for i in range(50):
        if random.choice([True, False]):  # Randomly decide if the user will edit their posts
            user_posts = [post_id for post_id, author in post_ids if author == f"user{i}"]
            for post_id in user_posts:
                edit_post(f"user{i}", post_id, f"Updated Title {i}", f"Updated Content {i}")
                time.sleep(0.1)

    # Create comments
    comment_ids = []
    for i in range(50):
        num_comments = random.randint(0, 5)  # Each user can create between 0 to 5 comments
        for _ in range(num_comments):
            post_id, _ = random.choice(post_ids)
            comment_id = create_comment(f"user{i}", post_id, f"Comment {i}")
            comment_ids.append((comment_id, f"user{i}"))
            time.sleep(0.1)

    # Like posts
    for i in range(50):
        num_likes = random.randint(0, 5)  # Each user can like between 0 to 5 posts
        for _ in range(num_likes):
            post_id, _ = random.choice(post_ids)
            like_post(f"user{i}", post_id)
            time.sleep(0.1)

    # Like comments
    for i in range(50):
        num_likes = random.randint(0, 5)  # Each user can like between 0 to 5 comments
        for _ in range(num_likes):
            comment_id, _ = random.choice(comment_ids)
            like_comment(f"user{i}", comment_id)
            time.sleep(0.1)

if __name__ == "__main__":
    test_endpoints()