import requests
import json
from datetime import datetime, timedelta
import time

# Fantasy points (change for custom leagues)
FGM = 2 # Field goal made
FGA = -1 # Field goal attempted
FTM = 1 # Free throw made
FTA = -1 # Free throw attempted
TPM = 1 # 3 pointer made
REB = 1 # Rebounds
AST = 2 # Assists
STL = 4 # Steals
BLK = 4 # Blocks
TO = -2 # Turnovers
PTS = 1 # Points

def fantasy_pt_calculator(fgm, fga, ftm, fta, tpm, reb, ast, stl, blk, to, pts):
    fpts = 0
    fpts += fgm * FGM
    fpts += fga * FGA
    fpts += ftm * FTM
    fpts += fta * FTA
    fpts += tpm * TPM
    fpts += reb * REB
    fpts += ast * AST
    fpts += stl * STL
    fpts += blk * BLK
    fpts += to * TO
    fpts += pts * PTS
    return fpts

# Set up dates for matches
def date_encode(date):
    return date.strftime("%G") + '-' + date.strftime("%m") + '-' + date.strftime("%d")

def extract_stats(response_json):
    fgm = int(response_json['data'][0]['fgm'])
    fga = int(response_json['data'][0]['fga'])
    ftm = int(response_json['data'][0]['ftm'])
    fta = int(response_json['data'][0]['fta'])
    tpm = int(response_json['data'][0]['fg3m'])
    reb = int(response_json['data'][0]['reb'])
    ast = int(response_json['data'][0]['ast'])
    stl = int(response_json['data'][0]['stl'])
    blk = int(response_json['data'][0]['blk'])
    to = int(response_json['data'][0]['turnover'])
    pts = int(response_json['data'][0]['pts'])
    return fgm, fga, ftm, fta, tpm, reb, ast, stl, blk, to, pts

# Players of interest:
# If you want to hard-code the player names, you can edit the list of players with their names.
players = []
player_ids = []

# If you are hard-coding the names, set this to False.
inputting = True

while inputting:
    inp_player = input('Enter the name of a player you would like to look at. Press enter again when done.')
    if inp_player != '':
        players.append(inp_player)
    else:
        inputting = False

# Get IDs of players
url = 'https://www.balldontlie.io/api/v1/players'
for i in players:
    params = {"search":i}
    response = requests.get(url, params=params)
    #print(response.json())
    response_json = response.json()['data'][0]['id']
    player_ids.append(response_json)

# How many games are we looking at?
target_games = int(input('How many games do you want to look at?'))

# Use the API to get the stats and fantasy points
fpts = 0
game_count = 0
days = 0
player_fpts = []

url = "https://www.balldontlie.io/api/v1/stats"
for i in player_ids:
    while game_count < target_games:
        # It searches for matches happening on each day, going backwards from 
        # today, until the target amount of games is reached.
        day = date_encode(datetime.now() - timedelta(days = days))
        params = {"start_date":day, "end_date":day, "player_ids[]":[i]}
        response = requests.get(url, params=params)
        try: 
            response_json = response.json()
            # If the total_count is 0, that means that no match was played. 
            if response_json['meta']['total_count'] > 0:
                # If a player is out/doesn't play, the match still appears in the 
                # API call. We must filter out matches with 0 mins played.
                if response_json['data'][0]['min'] != '00':
                    game_count += 1
                    fgm, fga, ftm, fta, tpm, reb, ast, stl, blk, to, pts = extract_stats(response_json)
                    fpts += fantasy_pt_calculator(fgm, fga, ftm, fta, tpm, reb, ast, stl, blk, to, pts)
        except:
            time.sleep(1)
            pass
        days += 1
    player_fpts.append(fpts)
    days = 0
    game_count = 0
    fpts = 0

# Sort the players from highest points to lowest points.
sorted_descending = sorted(range(len(player_fpts)), key=lambda k: player_fpts[k], reverse = True)
sorted_fpts = []
sorted_players = []
for i in sorted_descending:
    sorted_fpts.append(player_fpts[i])
    sorted_players.append(players[i])

# Output the points for each player (total & average)
print('Total fantasy points over the last', target_games, 'games.')
for i in range(len(sorted_players)):
    print(sorted_players[i] + ':', sorted_fpts[i])

print('\nAverage fantasy points over the last', target_games, 'games.')
for i in range(len(sorted_players)):
    print(sorted_players[i] + ':', sorted_fpts[i]/target_games)