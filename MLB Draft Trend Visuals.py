#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 16:53:39 2020

@author: stevennagy
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_early = pd.read_excel('Differences by Rounds.xlsx',sheet_name='Rounds 1-10')
df_late = pd.read_excel('Differences by Rounds.xlsx',sheet_name='Rounds 11-40')
df_all = pd.read_excel('Differences by Rounds.xlsx',sheet_name='All Rounds')
driveline_df = pd.read_excel('Differences by Rounds.xlsx',sheet_name='Driveline VA')


#adjust values to be percentage instead of overall count of players
total_early = df_early.groupby(['team_name','Overall_Rep']).agg({'Pct': 'sum'})
pct_early = total_early.groupby(level=0).apply(lambda x:
                                   100 * x / float(x.sum())).reset_index()
#create stacked bar chart for rounds 1-10    
pct_early.pivot_table(index='team_name',columns='Overall_Rep',values='Pct').plot.bar(stacked=True,cmap='Set1')
plt.legend(loc='upper center',bbox_to_anchor=(1.17,1.0))
plt.title('MLB Draft Trends Rounds 1-10',fontweight='bold',fontsize=14)
plt.xlabel('Organization',fontweight='bold')
plt.ylabel('% of Draft Type',fontweight='bold')
plt.show()

#print list of orgs that draft the most top D1
top_d1 = pct_early.loc[pct_early['Overall_Rep'] == 'Top D1']
top_d1 = top_d1.sort_values(by='Pct',ascending=False)
print(top_d1.head(30))


#adjust values to be percentage instead of overall count of players
total_late = df_late.groupby(['team_name','Overall_Rep']).agg({'Pct': 'sum'})
pct_late = total_late.groupby(level=0).apply(lambda x:
                                   100 * x / float(x.sum())).reset_index()
#create stacked bar chart for rounds 11-40    
pct_late.pivot_table(index='team_name',columns='Overall_Rep',values='Pct').plot.bar(stacked=True,cmap='Set1')
plt.legend(loc='upper center',bbox_to_anchor=(1.17,1.0))
plt.title('MLB Draft Trends Rounds 11-40',fontweight='bold',fontsize=14)
plt.xlabel('Organization',fontweight='bold')
plt.ylabel('% of Draft Type',fontweight='bold')
plt.show()

#print list of orgs that draft the most top D1 in later rounds
top_d1 = pct_late.loc[pct_late['Overall_Rep'] == 'Top D1']
top_d1 = top_d1.sort_values(by='Pct',ascending=False)
print(top_d1.head(30))


#adjust values to be percentage instead of overall count of players
total_all = df_all.groupby(['team_name','Overall_Rep']).agg({'Pct': 'sum'})
pct_all = total_all.groupby(level=0).apply(lambda x:
                                   100 * x / float(x.sum())).reset_index()
#create stacked bar chart for all rounds    
pct_all.pivot_table(index='team_name',columns='Overall_Rep',values='Pct').plot.bar(stacked=True,cmap='Set1')
plt.legend(loc='upper center',bbox_to_anchor=(1.17,1.0))
plt.title('MLB Draft Trends All Rounds',fontweight='bold',fontsize=14)
plt.xlabel('Organization',fontweight='bold')
plt.ylabel('% of Draft Type',fontweight='bold')
plt.show()



#print list of orgs that draft the most top D1
top_d1 = pct_all.loc[pct_all['Overall_Rep'] == 'Top D1']
top_d1 = top_d1.sort_values(by='Pct',ascending=False)
print(top_d1.head(30))
#add a column to pct_all that is the sum of all non-top D1 picks
top_d1['Non_Top_D1'] = 100 - top_d1.Pct
print(top_d1.head(30))
top_d1 = pd.merge(left=top_d1,right=driveline_df,left_on='team_name',right_on='Team')

#see if there is relationship between not drafting top D1 and Driveline value added
sns.regplot(x=top_d1.Non_Top_D1,y=top_d1.Millions)
plt.xlabel('% of Players Not Drafted From Top D1 Conferences',fontweight='bold')
plt.ylabel('Driveline Value Added in Millions ($)',fontweight='bold')
plt.title('Relationship Between Driveline Value Added \n and % of Non-D1 Players Drafted',fontweight='bold',fontsize=14)
for i, txt in enumerate(top_d1.team_name):
    plt.annotate(txt, (top_d1.Non_Top_D1[i],top_d1.Millions[i]))
plt.show()


#create another bar chart to show how teams draft top D1 players compared to league average
lg_avg = df_all.loc[df_all['Overall_Rep'] == 'Top D1']
lg_avg.pivot_table(index='team_name',columns='Overall_Rep',values='Ab_Bel_Avg').plot.bar(legend=None)
plt.title('How Teams Draft From Top D1 Conferences \n Compared to The League',fontweight='bold',fontsize=14)
plt.xlabel('Organization',fontweight='bold')
plt.ylabel('% Drafted Above or Below Average',fontweight='bold')
plt.axhline(y=0,color='black',linestyle='dashed',linewidth=1)
plt.show()


#create new dataframe in order to compare how team draft trends change from early to late
pct_early  = pct_early.loc[pct_early['Overall_Rep'] == 'Top D1']
pct_late = pct_late.loc[pct_late['Overall_Rep'] == 'Top D1']
diff_df = pd.merge(left=pct_early,right=pct_late,left_on='team_name',right_on='team_name')
diff_df['Diff_Early_Late'] = diff_df.Pct_x - diff_df.Pct_y
#print(diff_df.sort_values(by='Diff_Early_Late',ascending=False).head(30))

#visualize the teams with biggest difference
diff_df.pivot_table(index='team_name',columns='Overall_Rep_x',values='Diff_Early_Late').plot.bar(legend=None)
plt.title('Teams with Biggest Differences in \n Top D1 Conference Draftees From Rounds 1-10 to 11-40',fontweight='bold',fontsize=14)
plt.xlabel('Organization',fontweight='bold')
plt.ylabel('% Change From Rounds 1-10 to 11-40',fontweight='bold')
plt.show()



