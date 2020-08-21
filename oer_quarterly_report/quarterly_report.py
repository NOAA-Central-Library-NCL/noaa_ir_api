from datetime import datetime
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

"""
Script is used to generate report and charts for OER on a quarterly basis.
"""

# import custom scripts
from stats import StatsData
from api_query import RepositoryQuery
from article_monthly_update import transform_cdc_report

# create DataFrames

q = RepositoryQuery()
q.fields = [ 'PID', 'mods.title', 'mods.type_of_resource',
'mods.related_series', 'mods.sm_digital_object_identifier']

s = StatsData('mods.sm_localcorpname', pid_info=q.pid_dict)
oer_df = s.get_df('4')

# convert to to allow for merging on pid
oer_df['PID'] = oer_df['PID'].astype('int')
oer_df['mods.related_series'] = oer_df['mods.related_series'].str.join('')

oer_df['mods.sm_digital_object_identifier'] \
    = oer_df['mods.sm_digital_object_identifier'].str.join('')

current_cdc_file = input('Path to current CDC Report: ')
cdc_df = transform_cdc_report(current_cdc_file)

merged_data = oer_df.merge(
    cdc_df,
    left_on='PID',
    right_on='PID'
    )

# reindex
merged_data = merged_data[['mods.title', 'PID', 'DOI','mods.type_of_resource',
    'Stacks Downloads', 'Stacks Views', 'Date Added', 'Months in IR',
    'Avg Downloads per Month', 'Avg Views per Month', 'mods.ss_publishyear',
    'mods.related_series']]

# rename columns
merged_data = merged_data.rename(columns={'mods.title':'Title', 'PID': 'Link'
    'mods.type_of_resource': 'Document Type', 'Stacks Downloads': 'Downloads',
    'Stacks Views': 'Views', 'mods.ss_publishyear': 'Published Year',
    'mods.related_series':'Series'})

today = datetime.now().strftime('%m-%d-%Y')
merged_data.to_csv(r'oer_usage_report-{today}.csv')
