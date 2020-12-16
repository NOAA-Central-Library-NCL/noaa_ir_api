import sys
import os
from stats import StatsData


collection_pid = sys.argv[1]


s = StatsData('mods.sm_localcorpname',
    pid_info={
    # 'NMFS': '5',
    # 'NOS': '8',
    # 'OAR': '7',
    'NWS':'6',
    # 'NESDIS':'9',
    'CIs': '23649'}
)

df = s.get_df(collection_pid)
df['fy20_datetime'] = df['fgs.createdDate'].astype('datetime64')

# convert type of resource to string (from list)
df['mods.type_of_resource'] = df['mods.type_of_resource'].str.join('') 
# remove video 
df = df[~df['mods.type_of_resource'].str.contains('Video')]

# restrict to up until fy20
df = df.set_index(df['fy20_datetime'])
df = df.loc['2017-10-01': '2020-09-10']


# Total number of NOAA pubs per collection
noaa_pubs = df['mods.type_of_resource']

# Total number of JA per collection





# Total DOIs per collection (NCL assigned)
# Number of NOAA pubs ingested in FY20
# Number of JA ingested in FY20  
# Number of NOAA pubs ingested in FY20 per collection
# Number of JA ingested in FY20 per collection  




