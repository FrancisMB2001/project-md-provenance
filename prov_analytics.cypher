//Lineage of a Post 
MATCH path = ()-[*]->(post:Post {id: 17})
RETURN path;



//Number of Interactions of a User
MATCH path = ()<-[*]-(user:User{username: 'user1'})
RETURN path;



//All Edited Posts 
MATCH (post:Post)<-[:EDITED]-(action:Action)
RETURN post.id, post.title, COUNT(action) AS editCount
ORDER BY editCount, post.id DESC;



//Pair of Users with most Interactions with Each Other
MATCH (user1:User)-[r1*2..3]-(n:Post)-[r2*2..3]-(user2:User)
WHERE user1 < user2
RETURN user1.username AS User1, user2.username AS User2, COUNT(DISTINCT r1) + COUNT(DISTINCT r2) AS interactionCount
ORDER BY interactionCount DESC
LIMIT 5;



//Users Who Never Interacted with Each Other Directly
MATCH (user1:User), (user2:User)
WHERE user1 > user2
AND NOT EXISTS {
    MATCH (user1)-[r1*2..3]-(n:Post)-[r2*2..3]-(user2:User)
}
RETURN user1.username AS User1, user2.username AS User2
ORDER BY User1, User2;