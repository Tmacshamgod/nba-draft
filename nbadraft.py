from urllib2 import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url_template = "http://www.basketball-reference.com/draft/NBA_{year}.html"
draft_df = pd.DataFrame()

for year in range(1966, 2016):
    url = url_template.format(year=year)
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html5lib')
    column_headers = [th.getText() for th in 
                              soup.findAll('tr', limit=2)[1].findAll('th')]
    
    data_rows = soup.findAll('tr')[2:]
    player_data = [[td.getText() for td in data_rows[i].findAll('td')]
                        for i in range(len(data_rows))]
    
    df = pd.DataFrame(player_data, columns=column_headers)
    df.insert(0, 'Draft_Yr', 2014)
    draft_df = draft_df.append(df, ignore_index=True)

    draft_df = draft_df.convert_objects(convert_numeric=True)
    draft_df = draft_df[draft_df.Player.notnull()]
    draft_df = draft_df.fillna(0)
    draft_df.rename(columns={'WS/48':'WS_per_48'}, inplace=True)
    draft_df.columns = draft_df.columns.str.replace('%', '_Perc')
    draft_df.columns.values[15:19] = [draft_df.columns.values[15:19][col] + 
                                              "_per_G" for col in range(4)]
    draft_df.loc[:,'Yrs':'AST'] = draft_df.loc[:,'Yrs':'AST'].astype(int)
    draft_df.drop('Rk', axis='columns', inplace=True)
    draft_df['Pk'] = draft_df['Pk'].astype(int) 
    
    draft_df.to_csv("draft_data_1966_to_2015.csv")
