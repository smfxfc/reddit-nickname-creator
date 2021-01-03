#! python3
"""
Gather the usernames of all subreddit posters by pulling username 
string from comments and posts. Check each username to existing 
username list, which is stored as a json file. If username is 
unique, generate it a random unique nickname and store in json dict 
as a key value pair.  
"""

import datetime
import time
import json

import praw

import config
import praw_functions as RI
from nickname_creator import create_unique_nickname

user_dict_file = "User_dict.json"
user_list_file = "User_list.json"
flair_templates_file = "Flair_templates.json"
sr = 'getnicknamed' # my subreddit name
# url for my subreddit post that updates every loop to display subreddit stats
submission_url = "https://www.reddit.com/r/getnicknamed/comments/knm14f/at_this_time/?utm_source=share&utm_medium=web2x&context=3"

while True:
    start = time.time()
    
    # open local json files which store username+nickname info
    with open(user_list_file) as json_file:
        initial_user_list = json.load(json_file)
    with open(user_dict_file) as json_file:
        user_dict = json.load(json_file)
    with open(flair_templates_file) as json_file:
        flair_templates_list = json.load(json_file)

    # initiate Reddit instance
    r = RI.bot_login()

    # scrape comments+submissions for new users. returns updated user list and count of new users added during this loop
    new_user_list, comments_users_added = RI.add_users_by_comments(r, sr, initial_user_list)
    new_user_list, submissions_users_added = RI.add_users_by_submissions(r, sr, new_user_list)

    # creates unique nicknames for new users. It returns an updated username+nickname dict
    user_dict = RI.update_nickname_dict(r, sr, user_dict, new_user_list)

    # praw-specific requirement to generate a flair template before assigning it to a user
    for template in r.subreddit(sr).flair.templates:
        if not template in flair_templates_list:
            flair_templates_list.append(template)

    # save updated json files which will be used next loop 
    with open(user_dict_file, 'w') as json_file:
        json.dump(user_dict, json_file)
    with open(user_list_file,'w') as json_file:
        json.dump(new_user_list, json_file)
    with open(flair_templates_file, 'w') as json_file:
        json.dump(flair_templates_list, json_file)
    
    # update my pinned subreddit post to show current subreddit username/nickname stats
    submission = r.submission(url=submission_url)
    running_user_count = len(new_user_list)
    last_user = new_user_list[-1]    
    edited_body = (
        f"""This subreddit has given a nickname to {running_user_count} users (and counting!).\n\n\n"""
        f"""The latest user to receive a nickname is u/{last_user}. Their nickname is {user_dict[last_user]}.""")    
    submission.edit(edited_body)

    # end of current loop    
    end = time.time()
    time_elapsed = end - start
    print(f'Loop finished. Time elapsed: {time_elapsed}.\n'\
        f'New users added by comments this loop: {comments_users_added}.\n'\
        f'New users added by submissions this loop: {submissions_users_added}.\n'\
        f'Now sleeping for 60 seconds...\n'\
        f'*******************************')    
    time.sleep(60)