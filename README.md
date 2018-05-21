# Objective
Predict the scores and outcomes of FRC matches based off of prior results.

# Dataset
Data is scraped from [The Blue Alliance](https://www.thebluealliance.com). Input data is a 2 x 3 x 5 `(number of alliances per match, number of teams per alliance, number of datapoints per team)` tensor of data of the 2 alliances in a match, with 3 teams per alliance. For FIRST Powerup, each team has data on `Ranking Score`, the average number of ranking points per match, `Park/Climb Points`, `Autonomous Points`, `Ownership Points`, earned for having control of scale and switches, `Vault Points`, and `Disqualifications`. The network is intended to be reusable for future years, so the datapoints will change.

Output data is a 1 x 2 `(1, number of alliances)` vector with the score of each alliance in a match.
   
