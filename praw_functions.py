#! python3

import praw
import config
from nickname_creator import create_unique_nickname


def bot_login():
    # creates a Reddit instance
    r = praw.Reddit(
        username = config.username,
        password = config.password,
        client_id = config.client_id,
        client_secret = config.client_secret,
        user_agent = "smfxfc's nickname bot v0.1")
    return r


def add_users_by_comments(r, sr, user_list): # r=reddit instance, sr=subreddit name
    comment_users_added = 0
    for comment in r.subreddit(sr).comments(limit=1000):
        user = comment.author
        user = user.name
    
        if not user in user_list:
            user_list.append(user)
            comment_users_added += 1
            print(f"Added {user} to user list.")
    
    return user_list, comment_users_added

def add_users_by_submissions(r, sr, user_list): # same function as add_users_by_comments, but for submissions
    submissions_users_added = 0
    for submission in r.subreddit(sr).new(limit=1000):
        if not submission.author: # for edge cases where submission author doesn't exist - this mostly relates to deleted submissions
            continue
        else:
            user = submission.author.name
        
        if not user in user_list:
            user_list.append(user)
            submissions_users_added += 1
            print(f"Added {user} to user list.")

    return user_list, submissions_users_added


def create_flair(r, sr, user_dict, username): # take username input and generate a flair based on their key-value pair nickname
    random_color = "\"%03x\" % random.randint(0, 0xFFF)" # flair colors didn't end up working- iirc it is no longer supported by praw api 
    nickname = user_dict[username]
    # creates flair template for this nickname
    user_flair_template = r.subreddit(sr).flair.templates.add(nickname,background_color=random_color, text_color=random_color, css_class=nickname)
    r.subreddit(sr).flair.set(username, text=nickname, css_class=nickname)
    print(f"Set {user_flair_template} flair for {username}")


def update_nickname_dict(r, sr, user_dict, user_list):
    for user in user_list: # for users in list of users. when function is called, the list has been updated for new usernames, dict has not
        
        if not user in list(user_dict.keys()): # check is user already is in dict
            user_dict[user] = 'To add'
        if not user_dict[user]: # any usernames that have a None val for whatever reason
            user_dict[user] = 'To add'
        
        if user_dict[user] == "To add":
            user_nickname = create_unique_nickname(list(user_dict.values())) # generates nickname, and checks if nickname already exists in dict.values(). probably best to not call a function within a function, so should change if revise code
            print(f"User {user} given unique nickname: {user_nickname}")        
            user_dict[user] = user_nickname
            create_flair(r, sr, user_dict, user) # again probably not great to call a function in another function like this
    return user_dict
