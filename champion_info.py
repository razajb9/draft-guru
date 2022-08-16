#!/usr/bin/env python
# coding: utf-8

# In[35]:


import pandas as pd
import numpy as np


# In[36]:


champion_pool = ['Aatrox',
 'Ahri',
 'Akali',
 'Akshan',
 'Alistar',
 'Amumu',
 'Anivia',
 'Aphelios',
 'Ashe',
 'Azir',
 'Bard',
 'BelVeth',
 'Blitzcrank',
 'Brand',
 'Braum',
 'Caitlyn',
 'Camille',
 'Cassiopeia',
 'Corki',
 'Darius',
 'Diana',
 'Dr. Mundo',
 'Draven',
 'Elise',
 'Ezreal',
 'Fiora',
 'Galio',
 'Gangplank',
 'Gnar',
 'Gragas',
 'Graves',
 'Gwen',
 'Hecarim',
 'Irelia',
 'Janna',
 'Jarvan IV',
 'Jax',
 'Jayce',
 'Jhin',
 'Jinx',
 'KaiSa',
 'Kalista',
 'Karma',
 'Karthus',
 'Kassadin',
 'Kayle',
 'Kayn',
 'Kennen',
 'KhaZix',
 'Kindred',
 'Kled',
 'KogMaw',
 'LeBlanc',
 'Lee Sin',
 'Leona',
 'Lillia',
 'Lissandra',
 'Lucian',
 'Lulu',
 'Miss Fortune',
 'Mordekaiser',
 'Morgana',
 'Nami',
 'Nasus',
 'Nautilus',
 'Neeko',
 'Nidalee',
 'Nilah',
 'Nocturne',
 'Olaf',
 'Orianna',
 'Ornn',
 'Pantheon',
 'Poppy',
 'Pyke',
 'Qiyana',
 'Rakan',
 'RekSai',
 'Rell',
 'Renata Glasc',
 'Renekton',
 'Riven',
 'Rumble',
 'Ryze',
 'Samira',
 'Sejuani',
 'Senna',
 'Seraphine',
 'Sett',
 'Shen',
 'Shyvana',
 'Singed',
 'Sion',
 'Sivir',
 'Skarner',
 'Sona',
 'Soraka',
 'Swain',
 'Sylas',
 'Syndra',
 'Tahm Kench',
 'Taliyah',
 'Talon',
 'Taric',
 'Thresh',
 'Tristana',
 'Trundle',
 'Tryndamere',
 'Twisted Fate',
 'Twitch',
 'Udyr',
 'Varus',
 'Vayne',
 'Veigar',
 'Vex',
 'Vi',
 'Viego',
 'Viktor',
 'Vladimir',
 'Volibear',
 'Wukong',
 'Xayah',
 'Xin Zhao',
 'Yasuo',
 'Yone',
 'Yuumi',
 'Zac',
 'Zed',
 'Zeri',
 'Ziggs',
 'Zilean',
 'Zoe']


# In[55]:


champid_dict = {}
valid_ids = []
for i in range(len(champion_pool)):
    champid_dict[champion_pool[i]] = i
    valid_ids.append(i)


# In[56]:


def champion_id_from_name(champion_name):
    """
    args: 
        (string): champion name without apostrophes
    returns:
        (int): id of requested champion if no champ can be found, returns NULL
    """
    try:
        return champid_dict[champion_name]
    except KeyError:
        return None


# In[58]:


def champion_name_from_id(champion_id):
    """
    args: 
        (int): champion id
    returns:
        (string): champion name without apostrophes of requested id if no id can be found, returns NULL
    """
    try:
        return champion_pool[champion_id]
    except IndexError:
        return None


# In[1]:


def valid_champion_id(champion_id):
    """
    args: 
        (int): champion id
    returns:
        (bool): if champ id exists return True, if not False
    """
    try:
        x = champion_pool[champion_id]
        return True
    except IndexError:
        return False


# In[64]:


def get_ids():
    return valid_ids


# In[ ]:




