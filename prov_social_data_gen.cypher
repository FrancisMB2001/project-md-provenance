// Load data from CSV
LOAD CSV WITH HEADERS FROM 'file:///artifacts.csv' AS row

// Parse the inputs_json fields
WITH row, apoc.convert.fromJsonMap(row.inputs_json) AS inputs

// Create Action nodes, only some nodes will have a post_id or a comment_id
MERGE (action:Action {id: row.id, computed_at: row.computed_at, name: row.fn_name, username: inputs.user_username})
ON CREATE SET 
              action.post_id = CASE WHEN inputs.post_id IS NOT NULL THEN inputs.post_id ELSE NULL END,
              action.comment_id = CASE WHEN inputs.comment_id IS NOT NULL THEN inputs.comment_id ELSE NULL END

// Create User nodes and establish the relations with registT and loginT Action nodes
FOREACH (_ IN CASE WHEN inputs.user_username IS NOT NULL THEN [1] ELSE [] END |
    MERGE (user:User {username: inputs.user_username})
    ON CREATE SET user.computed_at = row.computed_at
    FOREACH (_ IN CASE WHEN row.fn_name = 'registT' THEN [1] ELSE [] END |
        MERGE (action)-[:REGISTERED]->(user)
    )
    FOREACH (_ IN CASE WHEN row.fn_name = 'loginT' THEN [1] ELSE [] END |
        MERGE (user)-[:LOGGED_IN]->(action)
    )
)

// Create createPostT Action nodes
WITH row, action, inputs
WHERE row.fn_name = 'createPostT'
MERGE (author:User {username: inputs.user_username})
MERGE (author)-[:CALLS]->(action)
MERGE (post:Post {id: inputs.post_id, title: inputs.post_title, author: inputs.user_username, content: inputs.post_content, computed_at: row.computed_at})
MERGE (action)-[:CREATED]->(post);




// Load data from CSV
LOAD CSV WITH HEADERS FROM 'file:///artifacts.csv' AS row

// Parse the inputs_json fields
WITH row, apoc.convert.fromJsonMap(row.inputs_json) AS inputs

// Create Comment nodes and relationships for createCommentT actions
WITH row, inputs
WHERE row.fn_name = 'createCommentT'
MERGE (commenter:User {username: inputs.user_username})
MERGE (action: Action {name: 'createCommentT', username: inputs.user_username, comment_id: inputs.comment_id})
MERGE (commenter)-[:CALLS]->(action)
MERGE (comment:Comment {id: inputs.comment_id, content: inputs.comment_content, author: inputs.user_username, computed_at: row.computed_at})
MERGE (action)-[:CREATED]->(comment)
MERGE (post:Post {id: inputs.post_id})
MERGE (comment)-[:ON]->(post);




// Load data from CSV
LOAD CSV WITH HEADERS FROM 'file:///artifacts.csv' AS row

// Parse the inputs_json fields
WITH row, apoc.convert.fromJsonMap(row.inputs_json) AS inputs

// Create relationships for editPostT actions
WITH row, inputs
WHERE row.fn_name = 'editPostT'
MERGE (editor:User {username: inputs.user_username})
MERGE (action: Action {name: 'editPostT', username: inputs.user_username, post_id: inputs.post_id})
MERGE (post:Post {id: inputs.post_id})
MERGE (editor)-[:CALLS]->(action)
MERGE (action)-[:EDITED]->(post);




// Load data from CSV
LOAD CSV WITH HEADERS FROM 'file:///artifacts.csv' AS row

// Parse the inputs_json fields
WITH row, apoc.convert.fromJsonMap(row.inputs_json) AS inputs

// Create relationships for likePostT actions
WITH row, inputs
WHERE row.fn_name = 'likePostT'
MATCH (post:Post {id: inputs.post_id})
MERGE (action: Action {name: 'likePostT', username: inputs.user_username, post_id: inputs.post_id})
MERGE (liker:User {username: inputs.user_username})
MERGE (liker)-[:CALLS]->(action)
MERGE (action)-[:LIKED]->(post);




// Load data from CSV
LOAD CSV WITH HEADERS FROM 'file:///artifacts.csv' AS row

// Parse the inputs_json field using the APOC library
WITH row, apoc.convert.fromJsonMap(row.inputs_json) AS inputs

// Create relationships for likeCommentT actions
WITH row, inputs
WHERE row.fn_name = 'likeCommentT'
MATCH (comment:Comment {id: inputs.comment_id})
MERGE (action: Action {name: 'likeCommentT', username: inputs.user_username, comment_id: inputs.comment_id})
MERGE (liker:User {username: inputs.user_username})
MERGE (liker)-[:CALLS]->(action)
MERGE (action)-[:LIKED]->(comment)