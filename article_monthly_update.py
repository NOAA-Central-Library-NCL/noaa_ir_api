import sys, os
from datetime import datetime
import numpy as np
import pandas as pd

"""
It is required that you access to the Article Monthly Reports to run this script.
"""


def transform_cdc_report(cdc_report):
    """
    Transform cdc excel report into csv, dropping columns,
    deduplicating, and then output a pandas df.

    Parameters:
        cdc_report: CDC article Monthly Update

    Returns:
        pandas DataFrame
    """

    df = pd.read_excel(cdc_report, skiprows=15, parse_dates=['Date Added'])
    df = df.drop(columns=['Unnamed: 0', 'Collection', 'Vault Downloads',
        'Vault Views','Funding Type Code','Funding','PMCID','PMID',
        'PMC Downloads', 'Number of Updates','Date Last Updated',
        'Public Access Available On','Citations', 'Published Date'])
    df = df.drop_duplicates()

    today = pd.to_datetime('today')

    df['today'] = today

    # determine how long item has been in IR
    df['Months in IR'] = df['today'] - df['Date Added']
    df['Months in IR']= df['Months in IR'] / np.timedelta64(1, 'M')

    df['Date Added'] = df['Date Added'].dt.date

    # determine usage average in IR
    df['Avg Downloads per Month'] = df['Stacks Downloads'] / df['Months in IR']
    df['Avg Views per Month'] = df['Stacks Views'] / df['Months in IR']

    df = df.drop(columns=['today'])

    #recorder columns
    df = df[['Article', 'PID','DOI','Article Type',
     'Stacks Downloads', 'Stacks Views', 'Email',
    'Shares', 'Prints','Date Added','Months in IR',
    'Avg Downloads per Month', 'Avg Views per Month' ]]

    df = df.drop_duplicates()

    return df


if __name__ == "__main__":
    cdc_report = sys.argv[1]
    df = transform_cdc_report(cdc_report)
