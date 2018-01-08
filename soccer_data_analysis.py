
# Soccer Data Analysis
# I answered 5 questions which are normally asked in every new season

# Q1) List of European **Strikers** any club can purchase in jan' 17  to get instant boost good enough to get silverware
# Q2) List of European **Defenders** any club can purchase purchase in jan' 17
#     to get instant boost good enough to get silverware
# Q3) List of European **Goal Keepers** any club can purchase purchase in jan' 17
#     to get instant boost good enough to get silverware
# Q4) Which **leagues** have the best home advantage and home fan entertainment<br>
# Q5) Which **Teams** are best in entertaining their home fans

# We used kaggle database to get european football dataset from 2008-2016
# [European Soccer Database](https://www.kaggle.com/hugomathien/soccer)

import pandas as pd
import sqlite3
import pprint
pp = pprint.PrettyPrinter()


data = sqlite3.connect('database.sqlite')


match = pd.read_sql("SELECT * FROM Match", data)
match_df = pd.DataFrame(match)

league = pd.read_sql("SELECT * FROM League", data)
league_df = pd.DataFrame(league)

match_details_df = pd.merge(match_df, league_df, on='country_id', how='outer')

player_attributes = pd.read_sql("SELECT * FROM Player_Attributes", data)
player_attributes_df = pd.DataFrame(player_attributes)

player = pd.read_sql("SELECT * FROM Player", data)
player_df = pd.DataFrame(player)

player_total_df = pd.merge(player_df, player_attributes, on='player_api_id', how='outer')


# Since API id was same in table "Match" and table "Team"
# but the problem was name of both the columns were different, So column name is supposed to rename
# so that I can merge them with api id as same column name in both tables


team = pd.read_sql("SELECT * FROM Team", data)
team_df = pd.DataFrame(team)

new_col = match_df.columns.values
new_col[7] = 'team_api_id'
match_df.columns = new_col
team_total_df = pd.merge(team_df, match_df, on='team_api_id', how='outer')


# cleaning data types
player_attributes_df['date'] = pd.to_datetime(player_attributes_df['date'])


# Taking players who performed well recently as per 2016
# Since we are suppossed to find the best players to purchase as per 2017 transfer window
# (since the data we have is upto 2016)
# primary condition noticed as per purchase is that the player must be in his top most form in recent days,
# Player attribute table had the details for every year so we considered players according to their 2016 form

# In[33]:


def pick_year(x):
    z = str(x).split('-')[0]
    return int(z)


# correcting data frame
# Since player names are repeated we took most recent player attributes,
# we created datframes with unique players(with player id not with player names, since many players have common names)


player_attributes_df = player_attributes_df.sort_values(by='date')
player_attributes_df = player_attributes_df.drop(player_attributes_df[player_attributes_df['date'].map(pick_year)
                                                                      != 2016].index)


def arranging_data(s, l):
    for x in l:
        if x not in s:
            s.append(x)
            if len(s) == 10:
                return s


# 10 European Strikers any club shall purchase in jan' 17 to get instant boost good enough to get silverware


# best attacking players in europe according to their game-play and personal abilities
player_total_df['attack_grade'] = player_total_df[['finishing', 'shot_power', 'acceleration', 'aggression', 'stamina',
                                                   'agility', 'positioning', 'strength', 'volleys', 'curve',
                                                   'heading_accuracy', 'dribbling']].mean(axis=1)
player_total_df_attack_grade = player_total_df.sort_values(by=['attack_grade'], ascending=False)

list_attacker = []
print('Best strikers to purchase for european football in 2017 transfer window')
pp.pprint(arranging_data(list_attacker, player_total_df_attack_grade['player_name']))
print('')


# 10 European Defenders any club shall purchase in jan' 17 to get instent boost good enough to get silverware


# best defencive player to purchase in 2017 for european soccer according to their gameplay and personal abilities
player_total_df['defence_grade'] = player_total_df[['interceptions', 'marking', 'standing_tackle', 'sliding_tackle',
                                                    'long_shots', 'reactions', 'agility', 'jumping', 'stamina',
                                                    'long_passing', 'short_passing', 'interceptions', 'vision',
                                                    'positioning', 'agility']].mean(axis=1)
player_total_df_defence_grade = player_total_df.sort_values(by=['defence_grade'], ascending=False)

list_defender = []
print('Best defenders to purchase for european football in 2017 transfer window')
pp.pprint(arranging_data(list_defender, player_total_df_defence_grade['player_name']))
print('')


# 10 European Goal keeper any club shall purchase in jan' 17 to get instent boost good enough to get silverware


# best goalkeeper to purchase in europe according to their gameplay and personal abilities
player_total_df['gk_grade'] = player_total_df[['potential', 'agility', 'reactions', 'balance', 'gk_kicking',
                                            'gk_diving', 'gk_reflexes', 'gk_handling', 'gk_positioning']].mean(axis=1)
player_total_df_gk_grade = player_total_df.sort_values(by=['gk_grade'], ascending=False)

list_gk = []
print('Best goal keeper to purchase for european football in 2017 transfer window')
pp.pprint(arranging_data(list_gk, player_total_df_gk_grade['player_name']))
print('')


# leagues which have best home advantage


match_details_df_league = match_details_df.groupby('league_id')

home_away_goal_diff = match_details_df_league['home_team_goal'].mean() - match_details_df_league['away_team_goal'].mean()
league_df['home_away_goal_diff'] = [i for i in home_away_goal_diff]

print('European leagues where home ground effect is maximum')
print(league_df.sort_values(by='home_away_goal_diff', ascending=False).iloc[:5]['name'])
print("")


# Teams that are best in entertaining their home fans


match_details_df_team = team_total_df.groupby('team_api_id')
home_away_goal_diff_team = match_details_df_team['home_team_goal'].mean() - match_details_df_team['away_team_goal'].mean()
team_df['home_away_goal_diff'] = [i for i in home_away_goal_diff_team]
team_df = team_df.sort_values(by='home_away_goal_diff', ascending=False)

print('European teams where home ground effect is maximum')
print(team_df.iloc[:10]['team_long_name'])
print("")
