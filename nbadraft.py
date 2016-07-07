from urllib2 import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url = "http://www.basketball-reference.com/draft/NBA_2014.html"
html = urlopen(url)
soup = BeautifulSoup(html)
column_headers = [th.getText() for th in 
                          soup.findAll('tr', limit=2)[1].findAll('th')]

data_rows = soup.findAll('tr')[2:]
player_data = [[td.getText() for td in data_rows[i].findAll('td')]
                    for i in range(len(data_rows))]

df = pd.DataFrame(player_data, columns=column_headers)
df = df[df.Player.notnull()]
df.rename(columns={'WS/48':'WS_per_48'}, inplace=True)
df.columns = df.columns.str.replace('%', '_Perc')
df.columns.values[14:18] = [df.columns.values[14:18][col] + 
                                          "_per_G" for col in range(4)]
df = df.convert_objects(convert_numeric=True)
df = df[:].fillna(0)
df.loc[:,'Yrs':'AST'] = df.loc[:,'Yrs':'AST'].astype(int)
df.insert(0, 'Draft_Yr', 2014)
df.drop('Rk', axis='columns', inplace=True)
