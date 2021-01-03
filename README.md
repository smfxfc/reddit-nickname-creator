# reddit-nickname-creator
Generate nicknames for all users of www.reddit.com/r/getnicknamed

Step-by-step process:
1. Gather the usernames of all subreddit posters by pulling username string from comments and posts
2. Check each username to existing username list, which is stored as a json file. 
3. If username is not in list, generate a random unique nickname and store in json dict as a key value pair with the username.  
