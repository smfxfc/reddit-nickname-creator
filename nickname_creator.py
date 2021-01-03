#! python3
""" Using two json files (one which stores a list of prefixes,
one which stores a list of adjectives) generate a unique nickname
by concatenating random values from each list. """

import random
import json

def random_prefix():
    with open("prefixes.json") as r:
        data = json.load(r)
    prefix = random.choice(data)
    print(f"Randomly selected prefix: {prefix}")
    return prefix

def random_adjective():
    with open("adjectives.json") as r:
        data = json.load(r)
    adj = random.choice(data)
    print(f"Randomly selected adjective: {adj.capitalize()}")
    return adj.capitalize()

def create_unique_nickname(user_list):
    prefix = random_prefix()
    adjective = random_adjective()
    nickname = f"{prefix} {adjective}"
    if nickname in user_list: # to ensure no duplicate nicknames
        create_unique_nickname(user_list)
    else:
        return nickname
