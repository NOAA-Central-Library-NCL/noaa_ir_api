import sys, os
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


def reformat_column(column):

    return column.replace(' ','_').lower()

def get_count(column):
    """
    Get count of column passed.

    Returns:
        CSV of frequency table and
        matplotlib plot

    """

    # document type counts
    counts = df[column].value_counts() \
        .to_frame().reset_index().rename(columns={
        'index': column, column:'Count'})

    r_column = reformat_column(column)
    counts.to_csv(os.path.join('data',
        f'{r_column}_{qt_info}_doc_counts.csv'),
        index=False
        )

    #plot document type counts
    counts.plot.barh(
        x=column,
        y='Count',
        title= f'Total Count to Date (as of FY{qt_info})',
        legend=False
        ).invert_yaxis()

    plt.savefig(
        os.path.join('data',
        f'{r_column}_{qt_info}_doc_counts.png'),
        dpi=300)


def get_views(column):

    # total download and views
    total_views = df.groupby(column) \
        [['Views']].sum()

    total_views = total_views.sort_values(
        by='Views')

    # print out CSV
    r_column = reformat_column(column)
    total_views.to_csv(os.path.join('data',
        f'{r_column}_{qt_info}_view_to_date.csv'),
        )

    # print chart
    total_views.plot.barh(
        rot=0,
        title= f'Total Views to Date (as of FY{qt_info})',
        legend=False
        )

    plt.savefig(
        os.path.join('data',
        f'{r_column}_{qt_info}-view_to_date.png'),
        dpi=300)


if __name__ == "__main__":

    input_file = sys.argv[1]
    qt_info = sys.argv[2]

    df = pd.read_csv(input_file)
    
    get_count('Document Type')
    get_count('Published Year')

    get_views('Document Type')
    get_views('Published Year')
