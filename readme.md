# API Paths

# Create User
api.fabler.fm/users/
**HTTP Methods**: POST

**Required Fields:** username, email, password

# Retrieve comment thread 
api.fabler.fm/threadlist/episode_[object_id]

# Post Comments
<h2> Post comment onto an episode </h2>
api.fabler.fm/postcomment/episode_[object_id]

**HTTP Methods**: POST

**Required Fields:** comment

api.fabler.fm/postcomment/episode_[object_id]/parent_[parent_id]

**HTTP Methods**: POST

**Required Fields:** comment

<h2> Post comment onto a Publisher </h2>
api.fabler.fm/postcomment/publisher_[object_id]

**HTTP Methods**: POST

**Required Fields:** comment

api.fabler.fm/postcomment/publisher_[object_id]/parent_[parent_id]

**HTTP Methods**: POST

**Required Fields:** comment

<h2> Post comment onto a Podcast </h2>
api.fabler.fm/postcomment/podcast_[object_id]

**HTTP Methods**: POST

**Required Fields:** comment

api.fabler.fm/postcomment/podcast_[object_id]/parent_[parent_id]

**HTTP Methods**: POST

**Required Fields:** comment

# Vote
api.fabler.fm/vote/

**HTTP Methods**: POST

**Required Fields:** value, comment
