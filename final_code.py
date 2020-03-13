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


def plot_quartile_season_arrests(df):
    """
    Takes in the dataframe. Then creates a bar plot of the 
    average arrests per quartile of the season. The season
    is broken up into 4 quartiles: 1 (weeks 1-4), 2 (weeks 5-9),
    3 (weeks 10-14), 4 (weeks 15-17).

    """
    df['quartile'] = df['week_num']//5
    df['quartile'] = df['quartile'] + 1
    filtered = df[['arrests', 'quartile']]
    result = filtered.groupby('quartile')['arrests'].mean()
    sns.catplot(x='quartile', y='arrests', kind='bar',
                data=result.reset_index())
    plt.title("Average Arrests per Week in Season")
    plt.xlabel('Quartile of Season')
    plt.ylabel('Average Arrests')
    plt.savefig('quartile_arrest.png', bbox_inches='tight')


def plot_day_of_week_arrests(df, no_wednesday):
    """
    Takes in the dataframe and a varible of whether or not the 
    graph should include the one game played on Wednesday. 
    Then creates a bar plot of the average arrests per day of 
    the week.

    """
    filtered = df[['arrests', 'day_of_week']]
    if(no_wednesday):
        filtered = df[df['day_of_week'] != 'Wednesday']
    result = filtered.groupby('day_of_week')['arrests'].mean()
    sns.catplot(x='day_of_week', y='arrests', kind='bar',
                data=result.reset_index())
    plt.title("Average Arrests per Day of the Week")
    plt.xlabel('Day of the Week')
    plt.ylabel('Average Arrests')
    if(no_wednesday):
        plt.savefig('day_of_week_arrest.png', bbox_inches='tight')
    else:
        plt.savefig('day_of_week_arrest_wednesday.png', bbox_inches='tight')


def plot_time_of_game_arrests(df):
    """
    Takes in the dataframe. Then creates a bar plot of the 
    average arrests per time of the game. The time of the 
    game is determined by the hour in which the game started.

    """
    df['time_of_game_hour'] = df['gametime_local'].astype(str)
    df['time_of_game_hour'] = df['time_of_game_hour'].str[:2]
    filtered = df[['arrests', 'time_of_game_hour']]
    result = filtered.groupby('time_of_game_hour')['arrests'].mean()
    sns.catplot(x='time_of_game_hour', y='arrests', kind='bar',
                data=result.reset_index())
    plt.title("Average Arrests per Time of Game")
    plt.xticks(np.arange(9), ['12pm', '1pm', '2pm',
                              '3pm', '4pm', '5pm',
                              '6pm', '7pm', '8pm'])
    plt.xlabel('Time of Game')
    plt.ylabel('Average Arrests')
    plt.savefig('time_of_game_arrests.png', bbox_inches='tight')


def plot_stadium_arrests(df):
    """
    Takes in the dataframe. Then creates a bar plot of the 
    average arrests per NFL stadium. 

    """
    filtered = df[['home_team', 'arrests']]
    result = filtered.groupby('home_team')['arrests'].mean()
    sns.catplot(x='arrests', y='home_team', kind='bar',
                data=result.reset_index())
    plt.title("Average Arrests for Each NFL Stadium")
    plt.xlabel('Average Arrests')
    plt.ylabel('Stadium')
    plt.savefig('stadium_arrest.png', bbox_inches='tight')


def plot_home_team_win_arrests(df):
    """
    Takes in the dataframe. Then creates a bar plot of the 
    average arrests per whether or not the home team won 
    the game. 

    """
    df['home_team_win'] = df['home_score'] > df['away_score']
    filtered = df[['arrests', 'home_team_win']]
    result = filtered.groupby('home_team_win')['arrests'].mean()
    sns.catplot(x='home_team_win', y='arrests', kind='bar',
                data=result.reset_index())
    plt.title("Average Arrests Compared to a Home Team Win")
    plt.xlabel('Home Team Win')
    plt.ylabel('Average Arrests')
    plt.savefig('home_team_win_arrest.png', bbox_inches='tight')


def plot_score_difference_arrests(df):
    """
    Takes in the dataframe. Then creates a line plot of the 
    average arrests per the score difference. Score difference
    is determined by the home team's score minus the away 
    team's score. Therefore, a negative score indicates a home 
    team loss.

    """
    df['score_difference'] = df['home_score'] - df['away_score']
    filtered = df[['arrests', 'score_difference']]
    result = filtered.groupby('score_difference')['arrests'].mean()
    sns.relplot(x='score_difference', y='arrests', kind='line',
                data=result.reset_index())
    plt.title("Average Arrests Compared to Final Score Difference")
    plt.xlabel('Final Score Difference (negative number implies a home team loss)')
    plt.ylabel('Average Arrests')
    plt.savefig('score_difference_arrest.png', bbox_inches='tight')


def categorical_score_difference(df):
    """
    Takes in the dataframe and creates a new column that categorizes the score
    difference by field goal, one score, two score, or blowout. Then creates a
    bar plot of the categorical score differences vs the average number of
    arrests at games with those differences.
    """
    df['score_diff'] = abs(df['home_score'] - df['away_score'])
    df['score_cat'] = 'tie'
    df.loc[df['score_diff'] <= 3, 'score_cat'] = 'field goal'
    df.loc[(df['score_diff'] > 3) & (
        df['score_diff'] <= 8), 'score_cat'] = 'one score'
    df.loc[(df['score_diff'] > 8) & (
        df['score_diff'] <= 16), 'score_cat'] = 'two score'
    df.loc[df['score_diff'] > 16, 'score_cat'] = 'blowout'
    result = df.groupby('score_cat')['arrests'].mean()
    sns.catplot(x='score_cat', y='arrests',
                kind='bar', data=result.reset_index(), order=['field goal', 'one score', 'two score', 'blowout'])
    plt.xlabel('Score Difference')
    plt.ylabel('Average Arrests per Game')
    plt.title('Arrests per Game Based on Score Difference')
    plt.savefig('categorical_score_difference.png', bbox_inches='tight')


def plot_overtime_arrests(df):
    """
    Takes in the dataframe. Then creates a bar plot of the 
    average arrests per whether or not the game went into 
    overtime.

    """
    filtered = df[['arrests', 'OT_flag']]
    result = filtered.groupby('OT_flag')['arrests'].mean()
    sns.catplot(x='OT_flag', y='arrests', kind='bar',
                data=result.reset_index())
    plt.title(
        "Average Arrests Compared to Whether or Not the Game Went into Overtime")
    plt.xlabel('Overtime')
    plt.ylabel('Average Arrests')
    plt.savefig('overtime_arrest.png', bbox_inches='tight')


def plot_divisional_arrests(df):
    """
    Takes in the dataframe. Then creates a bar plot of the 
    average arrests per whether or not the game was a 
    divisional game.

    """
    filtered = df[['arrests', 'division_game']]
    result = filtered.groupby('division_game')['arrests'].mean()
    sns.catplot(x='division_game', y='arrests', kind='bar',
                data=result.reset_index())
    plt.title(
        "Average Arrests Compared to Whether or Not the Game was a Divisional Matchup")
    plt.xlabel('Divisional Matchup')
    plt.ylabel('Average Arrests')
    plt.savefig('divisional_arrest.png', bbox_inches='tight')


def main():
    sns.set()
    data = pd.read_csv('arrests.csv')
    data = make_booleans(data)
    yearly_average(data)
    weekly_average(data)
    plot_winning_arrests_season(data)
    plot_winning_arrests_total(data)
    plot_quartile_season_arrests(data)
    plot_day_of_week_arrests(data, False)
    plot_day_of_week_arrests(data, True)
    plot_time_of_game_arrests(data)
    plot_stadium_arrests(data)
    plot_home_team_win_arrests(data)
    plot_score_difference_arrests(data)
    plot_overtime_arrests(data)
    plot_divisional_arrests(data)
    categorical_score_difference(data)


if __name__ == '__main__':
    main()
