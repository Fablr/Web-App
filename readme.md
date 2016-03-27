# API Paths

# Register User
/users/

**HTTP Methods:** POST

**Required Fields:** username, email, password

# Register User through Facebook/Twitter
/{backend}/?access_token={access_token}

**HTTP Methods:** POST

# Retrieve current user's profile
/userprofile/current/

**HTTP Methods:** GET

# Retrieve/Update specific user's profile
/userprofile/{user_id}/

**HTTP Methods:** GET, PATCH

**Optional Fields:** username={username}, email={email address}, first_name={user first name}, last_name={user last name}, birthday={user birthday}

# Retrieve Publishers
/publisher/

**HTTP Methods:** GET

# Retrieve specific Publisher
/publisher/{publisher_id}/

**HTTP Methods:** GET

# Retrieve Podcasts
/podcast/

**HTTP Methods:** GET

**Filters:** ?publisher={publisher_id}

# Retrieve specific Podcast
/podcast/{podcast_id}/

**HTTP Methods:** GET

# Retrieve/Add comments for a Podcast
/podcast/{podcast_id}/comments/

**HTTP Methods:** GET, POST

**Required Fields:** comment={comment text}

**Optional Fields:** parent={parent_comment_id}

# Retrieve current user's subscribed Podcasts
/podcast/subscribed/

**HTTP Methods:** GET

# Read specific user's subscribed Podcasts
/userprofile/{user_id}/subscribed/

**HTTP Methods:** GET

# Subscribe/Unsubscribe current user to Podcast
/subscription/

**HTTP Methods:** POST

**Required Fields:** podcast={podcast_id}, active={[(true)|(false)]}

# Retrieve EpisodeSerializer
/episode/

**HTTP Methods:** GET

**Filters:** ?podcast={podcast_id}

# Retrieve specific Episode
/episode/{episode_id}/

**HTTP Methods:** GET

# Retrieve/Add comments for an Episode
/episode/{episode_id}/comments/

**HTTP Methods:** GET, POST

**Required Fields:** comment={comment_text}

**Optional Fields:** parent={parent_comment_id}

# Update episode receipt
/episodereceipt/

**HTTP Methods:** POST

**Required Fields:** episode={episode_id}, mark={time in episode currently reached}, completed={[(true)|(false)]}

# Vote on comment
/vote/

**HTTP Methods:** POST

**Required Fields:** comment={comment_id}, value={[(-1)|(0)|(1)]}

# Delete/Edit comment
/comment/{comment_id}/

**HTTP Methods:** PATCH, DELETE

**Required Fields:** comment={new comment text}

# Retrieve specific user's followers
/userprofile/{user_id}/followers/

**HTTP Methods:** GET

# Retrieve whom specific user is Following
/userprofile/{user_id}/following/

**HTTP Methods:** GET

# Set current user to follow specific user
/following/

**HTTP Methods:** POST

**Required Fields:** following={user_id}

# Have current user unfollow specific user
/following/{user_id}/

**HTTP Methods:** DELETE

# Retrieve global feed
/feed/

**HTTP Methods:** GET

# Retrieve specific user's feed
/feed/{user_id}/

**HTTP Methods:** GET
