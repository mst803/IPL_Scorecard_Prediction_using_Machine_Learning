import pandas as pd
df1=pd.read_csv("ipl_2008-2020_ball_by_ball.csv")
df2=pd.read_csv("ipl_2008-2020_matches.csv")
df=pd.merge(df1,df2,on='id')
df['date']=pd.to_datetime(df['date'])
filtered_data = df[df['date'].dt.year >= 2015]
df_2020=filtered_data[['id','inning','over','ball','batsman','bowler','batsman_runs','is_wicket','venue','toss_decision','date','batting_team','bowling_team']]
df_2020["Year"]=df_2020["date"].dt.year
df_2020.fillna("Rajasthan Royals",inplace=True)
df_2020.drop("date",axis=1,inplace=True)

df_22_23=pd.read_csv('IPL_2022_2023.csv')

selected_data=pd.concat([df_22_23,df_2020],axis=0)
selected_data.to_csv("final.csv",index=False)