#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random

def test_train_split():
    """
    test_train_split returns match ids split into groups: a training set and a test set.

    Returns:
        Dictionary {"training_ids":list(int),"validation_ids":list(int)}
    """
    
    match_pool = []
    for i in range(0,953):
        match_pool.append(i)

    #### 85% of the matches will be randomly selected to train
    training_ids = random.sample(match_pool, 810)
    
    validation_ids = []
    test_pool = []
    for i in match_pool:
        if match_pool[i] not in training_ids:
            validation_ids.append(match_pool[i])

    return {"training_ids":training_ids,"validation_ids":validation_ids}


def match_pool(selected_match_ids):
    """
    Args:
        selected_match_ids (list): list of either training ids or validation ids

        match_data (dictionary): dictionary containing two keys:
            "match_ids": list of match_ids for pooled matches
            "matches": list of pooled match data to process
    Builds a set of matchids and match data used during learning phase
    """

    selected_matches = []
    for match_id in selected_match_ids:
        match = get_matches(match_id)
        selected_matches.append(match)

    return {"match_ids":selected_match_ids, "matches":selected_matches}


# In[2]:


import json
with open('matches.json') as json_file:
    matches = json.load(json_file)
    
def get_matches(matchID):
    matchID = str(matchID)
    return matches[matchID]


# In[3]:


get_matches(17)


# In[ ]:




