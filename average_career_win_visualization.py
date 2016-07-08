import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

draft_df = pd.read_csv("draft_data_1966_to_2016.csv", index_col=0)
WS48_yrly_avg = [draft_df[draft_df['Draft_Yr']==yr]['WS_per_48'].mean()
                         for yr in draft_df.Draft_Yr.unique()]
sns.set_style("white")  
plt.figure(figsize=(12,9))
x_values = draft_df.Draft_Yr.unique()  
y_values = WS48_yrly_avg
itle = ('Average Career Win Shares Per 48 minutes by Draft Year (1966-2016)')
plt.title(title, fontsize=20)
plt.ylabel('Win Shares Per 48 minutes', fontsize=18)
plt.xlim(1966, 2016.5)
plt.ylim(0, 0.08)
plt.grid(axis='y',color='grey', linestyle='--', lw=0.5, alpha=0.5)
plt.tick_params(axis='both', labelsize=14)

# get rid of borders for our graph using seaborn's despine function
sns.despine(left=True, bottom=True) 
plt.plot(x_values, y_values)
plt.text(1966, -0.012,
         'Primary Data Source: http://www.basketball-reference.com/draft/'
         '\nAuthor: Jeff Zhang',
         fontsize=12)
plt.show()
