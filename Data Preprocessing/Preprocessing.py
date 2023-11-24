


import numpy as np
import pandas as pd
import random
import seaborn as sns
from fuzzywuzzy import fuzz


# In[64]:


df=pd.read_csv("final.csv")


# In[65]:


df['total_runs'] = df.groupby(['id', 'batting_team'])['batsman_runs'].transform('sum')


# In[66]:


print(df.Year.value_counts())


# In[67]:


df.shape


# In[68]:


df.head()


# In[69]:


df.describe()


# In[70]:


sns.boxplot(data=df,x='total_runs')


# In[71]:


df = df[(df['total_runs'] > 48) & (df['total_runs'] < 258)]


# In[72]:


sns.boxplot(data=df,x='total_runs')


# In[73]:


df.describe()


# In[61]:


# The max value of ball is 11(in a single over), But we later convert the max value of balls to 6
df.isnull().sum()


# In[62]:


# There is not a single null value in the dataset
df.info()


# In[76]:


df['batting_team'].value_counts()


# In[77]:


df['bowling_team'].value_counts()


# In[78]:


df['batting_team'].replace('Rising Pune Supergiant','Rising Pune Supergiants',inplace=True)
df['bowling_team'].replace('Rising Pune Supergiant','Rising Pune Supergiants',inplace=True)


# In[79]:


df['bowling_team'].value_counts()


# In[173]:


# There are 4 columns with catagorical values, later we convert them into numericals


# In[174]:


# Replacing the balls greater than 6 to a random number between 1-6
for i in df['ball']:
    if i>6:
        df['ball'].replace(i,random.randint(1,6),inplace=True)


# In[175]:


# Converting the object data type of toss_decision column to boolean values by bat as true and field as false
df['toss_decision']=df['toss_decision']=='bat'


# In[176]:


# There are same players and venues repeated with diffrend names, we need to replace those similar names using fuzzywuuzy library
def find_similar_names(names_list, similarity_threshold=80):
    name_dict = {}
    similar_names = set()

    for name in names_list:
        if name in similar_names:
            continue
        similar_names.add(name)
        similar_names_list = [name]
        for i in names_list:
            if i != name:
                similarity_score = fuzz.ratio(name, i)
                if similarity_score >= similarity_threshold:
                    similar_names.add(i)
                    similar_names_list.append(i)
        if len(similar_names_list) > 1:
            name_dict[name] = similar_names_list

    return name_dict


# In[177]:


# For vanue
v=sorted(df['venue'].unique())
dict_venue=find_similar_names(v, similarity_threshold=75)
# Print the dictionary
for key, value in dict_venue.items():
    print(key, ':', value)


# In[178]:


# making some manuel changes
dict_venue['MA Chidambaram Stadium']=['MA Chidambaram Stadium, Chepauk, Chennai',"MA Chidambaram Stadium, Chepauk"]
dict_venue['Eden Gardens']=['Eden Gardens, Kolkata']
dict_venue['Narendra Modi Stadium']=['Narendra Modi Stadium, Ahmedabad']
dict_venue['Arun Jaitley Stadium']=['Arun Jaitley Stadium, Delhi']
del (dict_venue['Holkar Cricket Stadium'])


# In[179]:


for key,value in dict_venue.items():
    for i in value:
        df["venue"].replace(i,key,inplace=True)


# In[180]:


sorted(df['venue'].unique())


# In[181]:


# For players
b=sorted(df['batsman'].unique())
dict_bat=find_similar_names(b, similarity_threshold=75)
print(dict_bat)


# In[182]:


# making some manuel changes
for i in ["batsman","bowler"]:
    df[i].replace('RV Patel','Ripal Patel',inplace=True)
    df[i].replace('HV Patel','Harshal Patel',inplace=True)
    df[i].replace('AR Patel','Axar Patel',inplace=True)
    df[i].replace('BA Stokes','Ben Stokes',inplace=True)
    df[i].replace('CR Woakes','Chris Woakes',inplace=True)
    df[i].replace('DA Warner','David Warner',inplace=True)
    df[i].replace('E Lewis','Evin Lewis',inplace=True)
    df[i].replace('HH Pandya','Hardik Pandya',inplace=True)
    df[i].replace('KH Pandya','Krunal Pandya',inplace=True)
    df[i].replace('I Sharma','Ishant Sharma',inplace=True)
    df[i].replace('JM Sharma','Jitesh Sharma',inplace=True)
    df[i].replace('MM Sharma','Mohit Sharma',inplace=True)
    df[i].replace('RG Sharma','Rohit Sharma',inplace=True)
    df[i].replace('YK Pathan','Yusuf Pathan',inplace=True)
    df[i].replace('IK Pathan','Irfan Pathan',inplace=True)
    df[i].replace('UT Yadav','Umesh Yadav',inplace=True)
    df[i].replace('J Yadav','Jayant Yadav',inplace=True)
    df[i].replace('SA Yadav','Suryakumar Yadav',inplace=True)
    df[i].replace('JC Buttler','Jos Buttler',inplace=True)
    df[i].replace('JDS Neesham','JD Neesham',inplace=True)
    df[i].replace('JD Unadkat','Jaydev Unadkat',inplace=True)
    df[i].replace('JO Holder','Jason Holder',inplace=True)
    df[i].replace('KA Pollard','Kieron Pollard',inplace=True)
    df[i].replace('M Shahrukh Khan','Shahrukh Khan',inplace=True)
    df[i].replace('M Shami','Mohammed Shami',inplace=True)
    df[i].replace('MC Henriques','Moises Henriques',inplace=True)
    df[i].replace('S Dube','S Dubey',inplace=True)
    df[i].replace('WP Saha','Wriddhiman Saha',inplace=True)
    df[i].replace('PJ Cummins','Pat Cummins',inplace=True)
    df[i].replace('SN Khan','Sarfaraz Khan',inplace=True)
    df[i].replace('TH David','Tim David',inplace=True)
    df[i].replace('V Kohli','Virat Kohli',inplace=True)
    df[i].replace('V Shankar','Vijay Shankar',inplace=True)
    df[i].replace('MR Marsh','Mitchell Marsh',inplace=True)
    df[i].replace('CJ Green','C Green',inplace=True)
    df[i].replace('GD Phillips','Glenn Phillips',inplace=True)
    df[i].replace('JR Hazlewood','Josh Hazlewood',inplace=True)
    df[i].replace('Mohsin Khan (2)','Mohsin Khan',inplace=True)
    df[i].replace('Arshad Khan (2)','Arshad Khan',inplace=True)

# Now we need to numerical encoding of batsman,bowler and venue

# For vanue we rank them based on their size from an external sources

stadium_size = {
    'Arun Jaitley Stadium': 16,
    'Barsapara Cricket Stadium, Guwahati': 12,
    'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow': 13,
    'Brabourne Stadium': 4,
    'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium': 11,
    'Dubai International Cricket Stadium': 10,
    'Eden Gardens': 25,
    'Feroz Shah Kotla': 14,
    'Green Park': 15,
    'Himachal Pradesh Cricket Association Stadium, Dharamsala': 9,
    'Holkar Cricket Stadium': 8,
    'JSCA International Stadium Complex': 17,
    'M Chinnaswamy Stadium': 18,
    'MA Chidambaram Stadium': 19,
    'Maharashtra Cricket Association Stadium': 20,
    'Narendra Modi Stadium': 27,
    'Dr DY Patil Sports Academy, Mumbai':21,
    'Punjab Cricket Association IS Bindra Stadium, Mohali': 6,
    'Rajiv Gandhi International Stadium, Uppal': 19,
    'Sardar Patel Stadium, Motera': 23,
    'Saurashtra Cricket Association Stadium': 7,
    'Sawai Mansingh Stadium': 5,
    'Shaheed Veer Narayan Singh International Stadium': 24,
    'Sharjah Cricket Stadium': 2,
    'Sheikh Zayed Stadium': 3,
    'Wankhede Stadium': 22
}


# In[183]:


# Now we replace the venue with the corresponding size value
df['venue_encoded']=df['venue']
for i,j in stadium_size.items():
    df['venue_encoded'].replace(i,j,inplace=True)


# In[184]:


# Encoding batsman column

# Calculate the total runs for each "batsman"
sum_runs = df.groupby('batsman')['batsman_runs'].sum()


# In[185]:


# Calculate the total wickets for each "batsman"
sum_wickets=df.groupby('batsman')['is_wicket'].sum()
     
batsman_constant=dict(round(sum_runs/(sum_wickets+1),2))


# In[186]:


# To unique identification of batsman
batsman_encoder={}
for k in range(len(batsman_constant)):
    for i,j in batsman_constant.items():
        if j==min(batsman_constant.values()):
            batsman_encoder[i]=k
            del batsman_constant[i]
            break


print(batsman_encoder)


# In[187]:


# Ecoding using batsman_encoder
df['batsman_encoded']=df['batsman']
for i,j in batsman_encoder.items():
    df['batsman_encoded'].replace(i,j,inplace=True)



# In[188]:


# Calculate the total balls by each "bowler"
sum_balls = df['bowler'].value_counts()



# In[189]:


# Calculate the total wickets for each "bowler"
sum_wickets = df.groupby('bowler')['is_wicket'].sum()
     
bowler_constant = dict(round(sum_balls/300+(sum_wickets+1),2))


bowler_encoder={}
for k in range(len(bowler_constant)):
    for i,j in bowler_constant.items():
        if j==min(bowler_constant.values()):
            bowler_encoder[i]=k
            del bowler_constant[i]
            break



# In[190]:


print(bowler_encoder)

# Ecoding using bowler_encoder
df['bowler_encoded']=df['bowler']
for i,j in bowler_encoder.items():
    df['bowler_encoded'].replace(i,j,inplace=True)



# In[191]:


df.duplicated().sum()


# In[192]:


df.drop_duplicates(inplace=True)


# In[193]:


df.duplicated().sum()


# In[163]:


df.info()


# In[162]:


df.to_csv("processed.csv",index=False)


# In[ ]:




