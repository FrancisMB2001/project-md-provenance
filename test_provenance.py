import requests
import threading
import random
import time

BASE_URL = "http://127.0.0.1:8000"


def register_user(username, password):
    response = requests.post(
        f"{BASE_URL}/register", json={"username": username, "password": password}
    )
    print(response.json())


def login_user(username, password):
    response = requests.post(
        f"{BASE_URL}/login", json={"username": username, "password": password}
    )
    print(response.json())


def create_post(username, title, content):
    response = requests.post(
        f"{BASE_URL}/posts",
        json={"title": title, "content": content, "author": username},
        params={"username": username},
    )
    print(response.json())
    return response.json().get("id")


def edit_post(username, post_id, title, content):
    response = requests.put(
        f"{BASE_URL}/posts/{post_id}",
        json={"id": post_id, "title": title, "content": content, "author": username},
        params={"username": username},
    )
    print(response.json())


def create_comment(username, post_id, content):
    response = requests.post(
        f"{BASE_URL}/comments",
        json={"post_id": post_id, "content": content, "author": username},
        params={"username": username},
    )
    print(response.json())
    return response.json().get("id")


def like_post(username, post_id):
    response = requests.post(
        f"{BASE_URL}/posts/{post_id}/like", params={"username": username}
    )
    print(response.json())


def like_comment(username, comment_id):
    response = requests.post(
        f"{BASE_URL}/comments/{comment_id}/like", params={"username": username}
    )
    print(response.json())


names_list = [
    "lion",
    "tiger",
    "elephant",
    "giraffe",
    "zebra",
    "panther",
    "cheetah",
    "eagle",
    "sparrow",
    "shark",
    "dolphin",
    "whale",
    "wolf",
    "fox",
    "red",
    "blue",
    "green",
    "yellow",
    "purple",
    "orange",
    "pink",
    "jump",
    "run",
    "dance",
    "swim",
    "fly",
    "crawl",
    "climb",
    "sing",
    "shout",
]

content_list = [
    "A lion jumped over the moon",
    "The tiger ran through the forest",
    "An elephant painted a masterpiece",
    "Giraffes danced in the starlight",
    "Zebras played chess on the savannah",
    "The panther composed a symphony",
    "Cheetahs raced against the wind",
    "An eagle wrote a novel",
    "A sparrow solved a mystery",
    "The shark sang an opera",
    "Dolphins built an underwater city",
    "A whale performed a ballet",
    "Wolves howled in harmony",
    "Foxes hosted a tea party",
    "The sky turned red with fireflies",
    "Blue oceans sparkled with magic",
    "Green forests whispered secrets",
    "Yellow fields glowed with sunlight",
    "Purple sunsets painted dreams",
    "Orange clouds drifted like balloons",
    "Pink flowers danced in the breeze",
    "The world jumped into a new era",
    "Running thoughts filled the air",
    "Dancing stars twinkled with delight",
    "Swimming ideas flowed endlessly",
    "Flying carpets soared above",
    "Crawling vines wrapped the tower",
    "Climbing mountains sang songs",
    "Singing echoes filled the canyon",
    "Shouting waves crashed ashore",
]


def test_endpoints():

    number_of_iteration = 10
    
    # Static test case
    register_user("static_user_1", "password")
    login_user("static_user_1", "password")
    post_id_1 = create_post("static_user_1", "Static Title 1", "Static Content 1")
    post_id_2 = create_post("static_user_1", "Static Title 2", "Static Content 2")
    edit_post(
        "static_user_1", post_id_1, "Updated Static Title 1", "Updated Static Content 1"
    )
    comment_id_1 = create_comment("static_user_1", post_id_1, "Static Comment 1")
    comment_id_2 = create_comment("static_user_1", post_id_1, "Static Comment 2")
    like_post("static_user_1", post_id_1)
    like_comment("static_user_1", comment_id_1)
    like_comment("static_user_1", comment_id_2)

    # Register users
    for i in range(number_of_iteration):
        threading.Thread(target=register_user, args=(f"user{i}", "password")).start()
        time.sleep(0.1)

    # Login users
    for i in range(number_of_iteration):
        threading.Thread(target=login_user, args=(f"user{i}", "password")).start()
        time.sleep(0.1)

    # Create posts
    post_ids = []
    for i in range(number_of_iteration):
        num_posts = random.randint(0, 5)  # Each user can create between 0 to 5 posts
        for _ in range(num_posts):
            post_id = create_post(
                f"user{i}",
                random.choice(names_list)
                + random.choice(names_list)
                + random.choice(names_list)
                + str(i),
                random.choice(content_list) + str(i),
            )
            post_ids.append((post_id, f"user{i}"))
            time.sleep(0.1)

    # Edit posts
    for i in range(number_of_iteration):
        if random.choice(
            [True, False]
        ):  # Randomly decide if the user will edit their posts
            user_posts = [
                post_id for post_id, author in post_ids if author == f"user{i}"
            ]
            for post_id in user_posts:
                edit_post(
                    f"user{i}",
                    post_id,
                    f"Updated Title - {random.choice(names_list) + random.choice(names_list) + random.choice(names_list)}",
                    f"Updated Content {random.choice(content_list)}",
                )
                time.sleep(0.1)

    # Create comments
    comment_ids = []
    for i in range(number_of_iteration):
        num_comments = random.randint(
            0, 5
        )  # Each user can create between 0 to 5 comments
        for _ in range(num_comments):
            post_id, _ = random.choice(post_ids)
            comment_id = create_comment(
                f"user{i}",
                post_id,
                f"Comment {random.choice(content_list) + random.choice(content_list)}",
            )
            comment_ids.append((comment_id, f"user{i}"))
            time.sleep(0.1)

    # Like posts
    for i in range(number_of_iteration):
        num_likes = random.randint(0, 5)  # Each user can like between 0 to 5 posts
        for _ in range(num_likes):
            post_id, _ = random.choice(post_ids)
            like_post(f"user{i}", post_id)
            time.sleep(0.1)

    # Like comments
    for i in range(number_of_iteration):
        num_likes = random.randint(0, 5)  # Each user can like between 0 to 5 comments
        for _ in range(num_likes):
            comment_id, _ = random.choice(comment_ids)
            like_comment(f"user{i}", comment_id)
            time.sleep(0.1)


if __name__ == "__main__":
    test_endpoints()
