# Fantasy NBA API
Using the balldontlie API to gather the stats of NBA players over the last few games, as well as calculating their fantasy points.

First, the user is asked for which players they want to track. Then, they are asked for how many games they want to track.
The API is called, retrieving the stats for each of the last games for each player. The amount of fantasy points for these games is calculated as well.
The total fantasy points and the average fantasy points over those games is shown. This would allow you to make a more informed decision on which players to pick up in your Fantasy NBA league.

I made this because ESPN Fantasy (the league that I use) only has values for total points over the last 7/15/30 days and the average points over the season. Since all the consistently good players have already been taken in the draft, I want to look at recent points to inform my decision on who to pick up as a free agent. The points over last 7/15/30 days does not work well as players could have played a different amount of games over that period of time. This means that a player who is slightly worse but that has played more games recently is favored over a better player who has played less games. This program fixes that, as it looks at the same amount of games for each player.

How to use it:
First, change the point values for each action at the top of the program if needed. 
If you want to write the player names in the program itself (without having to input it each time), then you can edit the "players" list and set "inputting" to False.
If you don't want to do that, then you can run the program and input the player names.
NOTE: the player names must be spelt correctly or else an error will occur.
Then, you can enter the amount of games you want to look at. For example, if you enter 5, then the program will look at the last 5 games for each player.
The program will collect the stats for each player and use the point values provided earlier to calculate the fantasy points for each player. This step might take a while due to the 60 calls/minute limitation of the balldontlie API.
Finally, it displays the total fantasy points and average fantasy points for each player.
