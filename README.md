# FRC MatchPredictor
Predict the scores of FRC matches based off of prior results.

## Dataset
Data is scraped from [The Blue Alliance](https://www.thebluealliance.com). Input data is a 2 x 3 x 5 `(number of alliances per match, number of teams per alliance, number of datapoints per team)` tensor of data of the 2 alliances in a match, with 3 teams per alliance. For FIRST Powerup, each team has data on `Ranking Score`, the average number of ranking points per match, `Park/Climb Points`, `Autonomous Points`, `Ownership Points`, earned for having control of scale and switches, `Vault Points`, and `Disqualifications`. The network is intended to be reusable for future years, so the datapoints will change.

Output data is a 1 x 2 `(1, number of alliances)` vector with the score of each alliance in a match.
   
## Architecture
The main program will be a Bayesian regression, but will be compared the results of a simple linear, fully-connected neural network. 

## Validation
Bayesian Regression will be validated using uncertainty estimates. Linear Network is validated using [10-fold cross validation](https://www.openml.org/a/estimation-procedures/1). Data from many completed matches comprises the dataset. 

## Dependencies
Install the [Tbapy](https://github.com/frc1418/tbapy/blob/master/README.md) module to scrape The Blue Alliance

    pip3 install tbapy

Install Pyro for stochastic variational inference. Requires PyTorch.
 
    pip3 install pyro-ppl