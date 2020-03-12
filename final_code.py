import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def make_booleans(data):
    """
    Takes in the data as a dataframe and returns a new dataframe with the
    'OT_flag' and 'divisional_game' columns as booleans.
    """
    data['OT_flag'] = (data['OT_flag'] == 'OT')
    data['division_game'] = (data['division_game'] == 'y')
    return data


def yearly_average(data):
    """
    Takes in the data and creates a bar plot of the average number of arrest
    for each year in the dataset.
    """
    df = data.groupby('season')['arrests'].mean()
    sns.catplot(x='season', y='arrests', data=df.reset_index(), kind='bar', )
    plt.ylabel('average arrests')
    plt.title('Average Arrests per Game each Season')
    plt.savefig('yearly_average.png', bbox_inches='tight')


def weekly_average(data):
    """
    Takes in the data and creates a bar plot of the average arrests in each
    week of the data.
    """
    data['season-week'] = data['season'].astype(
        str) + ' - ' + data['week_num'].astype(str)
    df = data.groupby('season-week')['arrests'].mean()
    sns.catplot(x='season-week', y='arrests',
                data=df.reset_index(), kind='bar', color='blue')
    plt.xticks([])
    plt.xlabel('weeks')
    plt.ylabel('average arrests')
    plt.title('Average Arrests per Game each Week')
    plt.savefig('weekly_average.png', bbox_inches='tight')


def get_home_record(df, by_season=True):
    """
    Takes in data and a boolean(set to True) of whether it should be grouped
    by season or not, and groups rows by home team with a column
    showing their record and whether they were a winning team. Returns the
    filtered dataframe.
    """
    df['home_win'] = df['home_score'] > df['away_score']
    df['home_win'] = df['home_win'].astype(int)
    if by_season:
        df['team(season)'] = df['home_team'] + \
            '(' + df['season'].astype(str) + ')'
        filtered = df[['team(season)', 'home_win', 'arrests']]
        filtered = filtered.groupby('team(season)').mean()
        filtered['winning'] = filtered['home_win'] > .5
        return filtered
    filtered = df[['home_team', 'home_win', 'arrests']]
    filtered = filtered.groupby('home_team').mean()
    filtered['winning'] = filtered['home_win'] > .5
    return filtered


def plot_winning_arrests_season(df):
    """
    Takes in the data and calls get_home_record() on it. Then creates a bar
    plot of the average arrests for the teams with a winning home record that
    season or teams with a losing home record.
    """
    df = get_home_record(df)
    result = df.groupby('winning')['arrests'].mean()
    sns.catplot(x='winning', y='arrests',
                data=result.reset_index(), kind='bar')
    plt.xticks(np.arange(2), ['Losing Team', 'Winning Team'])
    plt.xlabel('Per Season')
    plt.ylabel('average arrests')
    plt.title('Average Arrests per Game (Season)')
    plt.savefig('winning_arrests.png', bbox_inches='tight')


def plot_winning_arrests_total(df):
    """
    Takes in the data and calls get_home_record() with by_season set to False.
    Then creates a bar plaot of the average arrests for the teams with a
    winning home record over the 5 seasons vs teams witha  losing home record.
    """
    df = get_home_record(df, False)
    result = df.groupby('winning')['arrests'].mean()
    sns.catplot(x='winning', y='arrests',
                data=result.reset_index(), kind='bar')
    plt.xticks(np.arange(2), ['Losing Team', 'Winning Team'])
    plt.xlabel('5 Year Average')
    plt.ylabel('average arrests')
    plt.title('Average Arrests per Game (5 Year Total)')
    plt.savefig('winning_arrests_total.png', bbox_inches='tight')


def main():
    sns.set()
    data = pd.read_csv('arrests.csv')
    data = make_booleans(data)
    yearly_average(data)
    weekly_average(data)
    plot_winning_arrests_season(data)
    plot_winning_arrests_total(data)


if __name__ == '__main__':
    main()
