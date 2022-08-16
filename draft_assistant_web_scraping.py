#!/usr/bin/env python
# coding: utf-8

# In[10]:


## Load in the necessary libraries
import requests # pip install requests
from bs4 import BeautifulSoup as bs #pip install beautifulsoup4
import pandas as pd
import sqlite3 as sql


# In[11]:



path = "C:\\Users\\thebr\\Desktop\\492\\" 
csvpathlist = []
conn = sql.connect('draftguru.db')
c = conn.cursor()


# In[12]:


requestlist = ["https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=LCS+2022+Summer&PBH%5Btextonly%5D=Yes&_run=",
               "https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=LEC+2022+Summer&PBH%5Btextonly%5D=Yes&_run=",
               "https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=LPL+2022+Summer&PBH%5Btextonly%5D=Yes&_run=",
               "https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=LCK+2022+Summer&PBH%5Btextonly%5D=Yes&_run=",
               "https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=PCS+2022+Summer&PBH%5Btextonly%5D=Yes&_run=",
              "https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D=VCS+2022+Summer&PBH%5Btextonly%5D=Yes&_run="]
# The order is LCS (North America), LEC (Europe), LPL (China), LCK (Korea), PCS (Taiwan + Southeast Asia), VCS (Vietnam)
counter = 1
for html in requestlist:
    test = requests.get(html)
    soup = bs(test.content)
    table = soup.select('table#pbh-table.wikitable.plainlinks.hoverable-rows.column-show-hide-1')[0]
    table_df = pd.read_html(str(table))[0]
    table_df.columns = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35"]
    table_df = table_df.drop(["35","34"], axis = 1)
    
    if counter == 1:
        df = table_df
    else:
        df = pd.concat([df,table_df], ignore_index = True, sort = False)
        
    counter += 1
df.columns = ['Phase', "Blue","Red","Score","Winner","Patch","BB1","RB1","BB2","RB2","BB3","RB3","BP1","RP1-2","BP2-3","RP3","RB4",
              "BB4","RB5","BB5","RP4","BP4-5","RP5","BR1","BR2","BR3","BR4","BR5","RR1","RR2","RR3","RR4","RR5"]


# In[13]:


df


# In[14]:


lol = df.values.tolist()


# In[15]:


command = """CREATE TABLE IF NOT EXISTS
matchtable(Phase varchar(7), Blue varchar(21), Red varchar(21), Score varchar(5),
Winner int, Patch varchar(5), BB1 varchar(21), RB1 varchar(21), BB2 varchar(21),
RB2 varchar(21), BB3 varchar(21), RB3 varchar(21), BP1 varchar(21), RP1 varchar(21),
RP2 varchar(21), BP2 varchar(21), BP3 varchar(21), RP3 varchar(21), RB4 varchar(21),
BB4 varchar(21), RB5 varchar(21), BB5 varchar(21), RP4 varchar(21), BP4 varchar(21),
BP5 varchar(21), RP5 varchar(21), BR1 varchar(7), BR2 varchar(7),
BR3 varchar(7), BR4 varchar(7), BR5 varchar(7), RR1 varchar(7), RR2 varchar(7), 
RR3 varchar(7), RR4 varchar(7), RR5 varchar(7), primary key(Phase, Blue, Red, Score))"""
c.execute(command)


# In[16]:


command = """INSERT INTO matchtable VALUES"""

for match in lol:
    matchcommand =  "("
    for i in range(len(match)):
        if type(match[i]) != str:
            match[i] = str(match[i])
        if "'" in match[i]:
                match[i] = match[i].replace("'", "")
        if (i < 6 or i > 22) and i < 32:
            matchcommand = matchcommand + "'" + match[i] + "',"
        elif i == 32:
            matchcommand = matchcommand + "'" + match[i] + "')"
        else:
            
            if i == 13 or i == 14 or i == 21:
                x = match[i].split(", ")
                matchcommand = matchcommand + "'" + x[0] + "',"
                matchcommand = matchcommand + "'" + x[1] + "',"
            else:
                matchcommand = matchcommand + "'" + match[i] + "',"
        if "MISSING DATA" in matchcommand:
            matchcommand = matchcommand.replace("MISSING DATA", "NULL")
        elif "None" in matchcommand:
            matchcommand = matchcommand.replace("None", "NULL")
    command2 = command + matchcommand
    c.execute(command2)        


# In[135]:


c.execute('DROP TABLE matchtable')


# In[17]:


c.execute('SELECT * FROM matchtable')
results = c.fetchall()
query = "SELECT * FROM matchtable"
df2 = pd.read_sql_query(query, conn)
df2


# In[18]:


df2.to_csv(r"C:\\Users\\thebr\\Desktop\\492\\matchtable_8.11.22")


# In[19]:


df2list = df2.values.tolist()
champion_pool = set()
for match in df2list:
    for i in range(len(match)):
        if i >= 6 and i <=25:
            if match[i] != "NULL":
                champion_pool.add(match[i])
champion_pool = list(champion_pool)

champion_pool.sort()
champion_pool


# In[20]:


print(len(champion_pool))
chlist = []
champid_dict = {}
for i in range(len(champion_pool)):
    champid_dict[champion_pool[i]] = i
    chlist.append(champion_pool[i])
champid_dict


# In[21]:


champ_id = 0
count = 0
banned = 0
picked = 0


blue_side = 0
red_side = 0

wins = 0
r_wins = 0
b_wins = 0

prescence_list = []

roles = []
role_info = []

side_data = []

pos_data = []
BP1 = 0
BP2_3 = 0
BP4_5 = 0
RP1_2 = 0
RP3 = 0
RP4 = 0
RP5 = 0

BP1W = 0
BP2_3W = 0
BP4_5W = 0
RP1_2W = 0
RP3W = 0
RP4W = 0
RP5W = 0

for champion in champion_pool:
    role_info.append(champ_id)
    for match in df2list:
        for i in range(len(match)):
            if i>= 6 and i <=25:
                if champion == match[i]:
                    count += 1
                    if i < 12:
                        banned += 1
                    elif i < 18:
                        picked += 1
                        if i == 12:
                            blue_side += 1
                            BP1 += 1
                            role_info.append(match[26])
                            if match[4] == 1:
                                b_wins += 1
                                BP1W += 1
                        elif i == 13:
                            red_side += 1
                            RP1_2 += 1
                            role_info.append(match[31])
                            if match[4] == 2:
                                r_wins += 1
                                RP1_2W += 1
                        elif i == 14:
                            red_side += 1
                            RP1_2 += 1
                            role_info.append(match[32])
                            if match[4] == 2:
                                r_wins += 1
                                RP1_2W += 1
                        elif i == 15:
                            blue_side += 1
                            BP2_3 += 1
                            role_info.append(match[27])
                            if match[4] == 1:
                                b_wins += 1
                                BP2_3W += 1
                        elif i == 16:
                            blue_side += 1
                            BP2_3 += 1
                            role_info.append(match[28])
                            if match[4] == 1:
                                b_wins += 1
                                BP2_3W += 1
                        elif i == 17:
                            red_side += 1
                            RP3 += 1
                            role_info.append(match[33])
                            if match[4] == 2:
                                r_wins += 1
                                RP3W += 1
                    elif i < 22:
                        banned += 1
                    else:
                        picked += 1
                        if i == 22:
                            red_side += 1
                            RP4 += 1
                            role_info.append(match[34])
                            if match[4] == 2:
                                r_wins += 1
                                RP4W += 1
                        elif i == 23:
                            blue_side += 1
                            BP4_5 += 1
                            role_info.append(match[29])
                            if match[4] == 1:
                                b_wins += 1
                                BP4_5W += 1
                        elif i == 24:
                            blue_side += 1
                            BP4_5 += 1
                            role_info.append(match[30])
                            if match[4] == 1:
                                b_wins += 1
                                BP4_5W += 1
                        elif i == 25:
                            red_side += 1
                            RP5 += 1
                            role_info.append(match[35])
                            if match[4] == 2:
                                r_wins += 1
                                RP5W += 1
                                
    prescence_perc = (count / ((len(df2list)))) * 100            
    prescence_perc = float("{0:.3f}".format(prescence_perc))
    
    roles.append(role_info) # no. of times a champ appeared each role
    
    wins = r_wins + b_wins
    
    if picked != 0:
        winrate = (wins / picked) * 100
        winrate = float("{0:.3f}".format(winrate))
    else:
        winrate = 0
    prescence_list.append([champ_id, champion, prescence_perc, banned, picked, winrate])
    
    if red_side != 0:
        rwinrate = (r_wins / red_side) * 100
        rwinrate = float("{0:.3f}".format(rwinrate))
    else:
        rwinrate = 0
    if blue_side != 0:
        bwinrate = (b_wins / blue_side) * 100
        bwinrate = float("{0:.3f}".format(bwinrate))
    else: 
        bwinrate = 0
    
    side_data.append([champ_id, picked, blue_side, bwinrate, red_side, rwinrate])
    
    if BP1 != 0:
        bp1wr = (BP1W / BP1) * 100
        bp1wr = float("{0:.3f}".format(bp1wr))
    else: 
        bp1wr = 0
    if BP2_3 != 0:
        bp23wr = (BP2_3W / BP2_3) * 100
        bp23wr = float("{0:.3f}".format(bp23wr))
    else:
        bp23wr = 0
    if BP4_5 != 0:
        bp45wr = (BP4_5W / BP4_5) * 100
        bp45wr = float("{0:.3f}".format(bp45wr))
    else:
        bp45wr = 0
    if RP1_2 != 0:
        rp12wr = (RP1_2W / RP1_2) * 100
        rp12wr = float("{0:.3f}".format(rp12wr))
    else:
        rp12wr = 0
    if RP3 != 0:
        rp3wr = (RP3W / RP3) * 100
        rp3wr = float("{0:.3f}".format(rp3wr))
    else:
        rp3wr = 0
    if RP4 != 0:
        rp4wr = (RP4W / RP4) * 100
        rp4wr = float("{0:.3f}".format(rp4wr))
    else: 
        rp4wr = 0
    if RP5 != 0:
        rp5wr = (RP5W / RP5) * 100
        rp5wr = float("{0:.3f}".format(rp5wr))
    else:
        rp5wr = 0
    
    pos_data.append([champ_id, picked, BP1, BP2_3, BP4_5, RP1_2, RP3, RP4, RP5,
                          bp1wr, bp23wr, bp45wr, rp12wr, rp3wr, rp4wr, rp5wr])
    
    champ_id += 1
    count = 0
    banned = 0
    picked = 0


    blue_side = 0
    red_side = 0

    wins = 0
    r_wins = 0
    b_wins = 0
    
    role_info = []
    
    BP1 = 0
    BP2_3 = 0
    BP4_5 = 0
    RP1_2 = 0
    RP3 = 0
    RP4 = 0
    RP5 = 0

    BP1W = 0
    BP2_3W = 0
    BP4_5W = 0
    RP1_2W = 0
    RP3W = 0
    RP4W = 0
    RP5W = 0
    


# In[22]:


import numpy as np
import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt


# In[23]:


df1 = pd.DataFrame(prescence_list)
df1.columns = ['ChampID','Name','Presence','BanCount','PickCount', 'Winrate']
winrate = df1.Winrate.hist()
print('Distribution of Champion Winrate')
plt.show()
df1.describe()


# In[24]:


role_list = []

for i in range(len(roles)):
    topcnt = 0
    jngcnt = 0
    midcnt = 0
    botcnt = 0
    supcnt = 0
    for j in range(len(roles[i])):
        if roles[i][j] == 'Top':
            topcnt += 1
        elif roles[i][j] == 'Jungle':
            jngcnt += 1
        elif roles[i][j] == 'Mid':
            midcnt += 1
        elif roles[i][j] == 'Bot':
            botcnt += 1
        elif roles[i][j] == 'Support':
            supcnt += 1
        else:
            champid = i
    picks = topcnt + jngcnt + midcnt + botcnt + supcnt
    role_list.append([champid, topcnt, jngcnt,midcnt, botcnt, supcnt, picks])
    topcnt = 0
    jngcnt = 0
    midcnt = 0
    botcnt = 0
    supcnt = 0
df_roles = pd.DataFrame(role_list)
df_roles.columns = ['ChampID', 'Top', 'Jungle', 'Mid', 'Bot', 'Support', 'Picks']
df_roles


# In[25]:


df_pos_data = pd.DataFrame(pos_data)
df_pos_data
df_pos_data.columns = ["ChampID","Pick Count", "BP1", "BP2_3","BP4_5", "RP1_2",
                       "RP3", "RP4", "RP5", "bp1wr", "bp23wr", "bp45wr", 
                       "rp12wr", "rp3wr", "rp4wr", "rp5wr"]
#df3 = df_pos_data.drop(['Pick Count', "BP1", "BP2_3","BP4_5", "RP1_2", "RP3", 
                        #"RP4", "RP5"], axis = 1)
df_pos_data['bp1wr'].dropna()
plt.hist(df_pos_data.bp1wr)
plt.show()


# In[26]:


plt.hist(df_pos_data.bp23wr)
plt.show()


# In[27]:


plt.hist(df_pos_data.bp45wr)
plt.show()


# In[28]:


plt.hist(df_pos_data.rp12wr)
plt.show()


# In[29]:


plt.hist(df_pos_data.rp3wr)
plt.show()


# In[30]:


plt.hist(df_pos_data.rp4wr)
plt.show()


# In[31]:


plt.hist(df_pos_data.rp5wr)
plt.show()


# In[32]:


df_side_data = pd.DataFrame(side_data)
df_side_data.columns = ["champ_id", "picked", "blue_side", "bwinrate", 
                        "red_side", "rwinrate"]
df_side_data.describe()


# In[33]:


winrate = df_side_data.bwinrate.hist()
print('Distribution of Blue Side Champion Winrate')
plt.show()


# In[34]:


winrate = df_side_data.rwinrate.hist()
print('Distribution of Red Side Champion Winrate')
plt.show()


# In[35]:


df1.to_csv(r"C:\\Users\\thebr\\Desktop\\492\\Prescence_list")
df_roles.to_csv(r"C:\\Users\\thebr\\Desktop\\492\\Roles")
df_pos_data.to_csv(r"C:\\Users\\thebr\\Desktop\\492\\Pos_data")


# In[36]:


df2list


# In[36]:


#create a swain.ban df 
#create a swain.pick df
#resembling the swain bot tables so that I can do the first step data.matchpool import

df2list

pickid = 0
banid = 0

bantable = []
picktable = []

cx = []

for i in range(len(df2list)):
    cx1 = [0,0,[],[]]
    cx2 = [0,0,[],[]]
    cx3 = [0,0,[],[]]
    cx4 = [0,0,[],[]]
    cx5 = [0,0,[],[]]
    cx6 = [0,0,[],[]]
    cx7 = [0,0,[],[]]
    cx8 = [0,0,[],[]]
    cx9 = [0,0,[],[]]
    cx10 = [0,0,[],[]]
    
    matchID
    for j in range(len(df2list[i])):
        
        
        if j == 4:
            if df2list[i][j] == 1:
                sideWin = 1
                cx2[1] = 1
                cx3[1] = 1
                cx6[1] = 1
                cx7[1] = 1
                cx10[1] = 1
            else:
                sideWin = 0
                cx1[1] = 1
                cx4[1] = 1
                cx5[1] = 1
                cx8[1] = 1
                cx9[1] = 1
        elif j == 6 or j == 8 or j == 10:
            phase = 0
            sideID = 0
            try:
                cID = champid_dict[df2list[i][j]]
            except KeyError:
                cID = 'NULL'
            bantable.append([banid,i,cID,phase,sideID,sideWin])
            banid += 1
        elif j == 7 or j == 9 or j == 11:
            phase = 0
            sideID = 1
            try:
                cID = champid_dict[df2list[i][j]]
            except KeyError:
                cID = 'NULL'
            
            bantable.append([banid,i,cID,phase,sideID,sideWin])
            banid += 1
        elif j == 12:
            selectO = 1
            sideID = 0
            try:
                cID = champid_dict[df2list[i][j]]
            except KeyError:
                cID = 'NULL'
            
            cx1[0] = cID
            
            cx2[2].append(cID)
            cx3[2].append(cID)
            cx6[2].append(cID)
            cx7[2].append(cID)
            cx10[2].append(cID)
            
            cx4[3].append(cID)
            cx5[3].append(cID)
            cx8[3].append(cID)
            cx9[3].append(cID)
            
            picktable.append([pickid,i,cID,selectO,sideID,sideWin])
            pickid += 1
        elif j == 13 or j == 14:
            selectO = 1
            sideID = 1
            try:
                cID = champid_dict[df2list[i][j]]
            except KeyError:
                cID = 'NULL'
            
            if j == 13:
                cx2[0] = cID
            
                cx1[2].append(cID)
                cx4[2].append(cID)
                cx5[2].append(cID)
                cx8[2].append(cID)
                cx9[2].append(cID)

                cx3[3].append(cID)
                cx6[3].append(cID)
                cx7[3].append(cID)
                cx10[3].append(cID)
            else:
                cx3[0] = cID
            
                cx1[2].append(cID)
                cx4[2].append(cID)
                cx5[2].append(cID)
                cx8[2].append(cID)
                cx9[2].append(cID)

                cx2[3].append(cID)
                cx6[3].append(cID)
                cx7[3].append(cID)
                cx10[3].append(cID)
                
            picktable.append([pickid,i,cID,selectO,sideID,sideWin])
            pickid += 1
        elif j == 15 or j == 16:
            selectO = 2
            sideID = 0
            try:
                cID = champid_dict[df2list[i][j]]
            except KeyError:
                cID = 'NULL'
            
            if j == 15:
                cx4[0] = cID
            
                cx2[2].append(cID)
                cx3[2].append(cID)
                cx6[2].append(cID)
                cx7[2].append(cID)
                cx10[2].append(cID)

                cx1[3].append(cID)
                cx5[3].append(cID)
                cx8[3].append(cID)
                cx9[3].append(cID)
            else:
                cx5[0] = cID
            
                cx2[2].append(cID)
                cx3[2].append(cID)
                cx6[2].append(cID)
                cx7[2].append(cID)
                cx10[2].append(cID)

                cx1[3].append(cID)
                cx4[3].append(cID)
                cx8[3].append(cID)
                cx9[3].append(cID)
            
            picktable.append([pickid,i,cID,selectO,sideID,sideWin])
            pickid += 1
        elif j == 17:
            selectO = 2
            sideID = 1
            try:
                cID = champid_dict[df2list[i][j]]
            except KeyError:
                cID = 'NULL'
            
            cx6[0] = cID
            
            cx1[2].append(cID)
            cx4[2].append(cID)
            cx5[2].append(cID)
            cx8[2].append(cID)
            cx9[2].append(cID)

            cx2[3].append(cID)
            cx3[3].append(cID)
            cx7[3].append(cID)
            cx10[3].append(cID)
            
            picktable.append([pickid,i,cID,selectO,sideID,sideWin])
            pickid += 1
        elif j == 18 or j == 20:
            phase = 1
            sideID = 1
            try:
                cID = champid_dict[df2list[i][j]]
            except KeyError:
                cID = 'NULL'
            
            bantable.append([banid,i,cID,phase,sideID,sideWin])
            banid += 1
        elif j == 19 or j == 21:
            phase = 1
            sideID = 0
            try:
                cID = champid_dict[df2list[i][j]]
            except KeyError:
                cID = 'NULL'
            
            bantable.append([banid,i,cID,phase,sideID,sideWin])
            banid += 1
        elif j == 22:
            selectO = 3
            sideID = 1
            cID = champid_dict[df2list[i][j]]
            
            cx7[0] = cID
            
            cx1[2].append(cID)
            cx4[2].append(cID)
            cx5[2].append(cID)
            cx8[2].append(cID)
            cx9[2].append(cID)

            cx2[3].append(cID)
            cx3[3].append(cID)
            cx6[3].append(cID)
            cx10[3].append(cID)
            
            picktable.append([pickid,i,cID,selectO,sideID,sideWin])
            pickid += 1
        elif j == 23 or j == 24:
            selectO = 3
            sideID = 0
            cID = champid_dict[df2list[i][j]]
            
            if j == 23:
                cx8[0] = cID
            
                cx2[2].append(cID)
                cx3[2].append(cID)
                cx6[2].append(cID)
                cx7[2].append(cID)
                cx10[2].append(cID)

                cx1[3].append(cID)
                cx4[3].append(cID)
                cx5[3].append(cID)
                cx9[3].append(cID)
            else:
                cx9[0] = cID
            
                cx2[2].append(cID)
                cx3[2].append(cID)
                cx6[2].append(cID)
                cx7[2].append(cID)
                cx10[2].append(cID)

                cx1[3].append(cID)
                cx4[3].append(cID)
                cx5[3].append(cID)
                cx8[3].append(cID)
            
            picktable.append([pickid,i,cID,selectO,sideID,sideWin])
            pickid += 1
        elif j == 25:
            selectO = 4
            sideID = 1
            cID = champid_dict[df2list[i][j]]
            
            cx10[0] = cID
            
            cx1[2].append(cID)
            cx4[2].append(cID)
            cx5[2].append(cID)
            cx8[2].append(cID)
            cx9[2].append(cID)

            cx2[3].append(cID)
            cx3[3].append(cID)
            cx6[3].append(cID)
            cx7[3].append(cID)
            
            picktable.append([pickid,i,cID,selectO,sideID,sideWin])
            pickid += 1
    cx.append(cx1)
    cx.append(cx2)
    cx.append(cx3)
    cx.append(cx4)
    cx.append(cx5)
    cx.append(cx6)
    cx.append(cx7)
    cx.append(cx8)
    cx.append(cx9)
    cx.append(cx10)
    
#####    pick/banID, gameID, champID, selectOrder/banPhase(early = 0, late = 1), sideID (blue = 0, red = 1), sideWin
#### select order b1 = 1, b23 = 2, b45 = 3, r12 = 1, r3 = 2, r4 = 3, r5 = 4
    
        




# In[ ]:





# In[37]:


df_roles.to_csv(r"C:\\Users\\thebr\\Desktop\\492\\Roles")
df_pos_data.to_csv(r"C:\\Users\\thebr\\Desktop\\492\\Pos_data")


# In[38]:



appearedMatches = []

for i in range(len(df_side_data)):
    championI = []
    for j in range(len(picktable)):
        if picktable[j][2] == i:
            if picktable[j][1] not in championI:
                championI.append(picktable[j][1])
    appearedMatches.append(championI)
    
appearedMatches[0]


# In[39]:


df_pos_data


# In[40]:


champion_pool[119]


# In[41]:


bestbluepick = df_pos_data[['ChampID', 'Pick Count', 'BP1', 'bp1wr']]
bp1s = bestbluepick[bestbluepick['bp1wr'] > 50]
bp1s


# In[101]:


list_zeros = [0] * 131
pickedagainst = []
wonagainst = []

pickedwith = []
wonwith = []

for i in range(len(appearedMatches)):
    pa_ith = list_zeros
    wa_ith = list_zeros
    
    pw_ith = list_zeros
    ww_ith = list_zeros
    for l in range(len(cx)):
        print(cx[0])
        if cx[0] == i:
            for j in range(len(cx[2])):
                chID = cx[2][j]
                print(chID)
                pa_ith[chID] = pa_ith[chID] + 1
                if cx[1] == 1:
                    wa_ith[chID] = wa_ith[chID] + 1
            for j in range(len(cx[3])):
                chID = cx[3][j]
                pw_ith[chID] = pw_ith[chID] + 1
                if cx[1] == 1:
                    ww_ith[chID] = ww_ith[chID] + 1
    pickedagainst.append(pa_ith)
    wonagainst.append(wa_ith)
    pickedwith.append(pw_ith)
    wonwith.append(ww_ith)


# In[98]:


len(pickedagainst[0])


# In[94]:


wragainst = []
for i in range(len(pickedagainst)):
    wra = []
    for j in range(len(pickedagainst[i])):
        try:
            wr = wonagainst[i][j] / pickedagainst[i][j]
        except ZeroDivisionError:
            wr = 'NULL'
        wra.append(wr)
    wragainst.append(wra)


# In[95]:


wragainst[127]


# In[43]:


df_cx = pd.DataFrame(cx)
df_bantable = pd.DataFrame(bantable)
df_picktable = pd.DataFrame(picktable)


# In[43]:


matchID = 0
matches = {}
from champion_info import champion_id_from_name
for match in df2list:

    blue_bans = [champion_id_from_name(match[6]), champion_id_from_name(match[8]), champion_id_from_name(match[10]), 
                 champion_id_from_name(match[19]), champion_id_from_name(match[21])]
    red_bans = [champion_id_from_name(match[7]), champion_id_from_name(match[9]), champion_id_from_name(match[11]), 
                champion_id_from_name(match[18]), champion_id_from_name(match[20])]
    blue_picks = [champion_id_from_name(match[12]), champion_id_from_name(match[15]), champion_id_from_name(match[16]), 
                  champion_id_from_name(match[23]), champion_id_from_name(match[24])]
    red_picks = [champion_id_from_name(match[13]), champion_id_from_name(match[14]), champion_id_from_name(match[17]), 
                 champion_id_from_name(match[22]), champion_id_from_name(match[25])]
    
    winner = 0
    if match[4] == 2:
        winner = 1
                                
    matches[matchID] = {"id": matchID, "winner": winner, "blue":{"bans": blue_bans, "picks": blue_picks},
                        "red":{"bans": red_bans, "picks": red_picks}}
    matchID += 1


# In[44]:


matches


# In[45]:


import json
with open("matches.json", "w") as outfile:
    json.dump(matches, outfile)


# In[ ]:




