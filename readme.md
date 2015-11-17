# API Paths

# Register User through Fabler
api.fabler.fm/users/

**HTTP Methods:** POST

**Required Fields:** username, email, password

# Register User through Facebook
[POST] api.fabler.fm/[backend]/?access_token=[access_token]

**HTTP Methods:** POST

# Retrieve comment thread
api.fabler.fm/[episode|podcast|publisher]/[object_id]/comments/

**HTTP Methods:** GET

# Post Comments
api.fabler.fm/[episode|podcast|publisher]/[object_id]/comments/

**HTTP Methods:** POST

**Required Fields:** comment

**Optional Fields:** parent

# Vote
api.fabler.fm/vote/

**Required Fields:** value, comment
