# 10000-Player

A player for the [10000](https://en.wikipedia.org/wiki/Dice_10000) dice game.

It can be used for playing by running the interface.py file.

It currently scores on average 293 points at each turn, with the following scoring rules:

 - One 1: 100.
 - One 5: 50.
 - Three 1: 1000.
 - Three 2: 200.
 - Three 3: 300.
 - Three 4: 400.
 - Three 5: 500.
 - Three 6: 600.
 
 The agent is trained playing many turns updating a value function:
    v[d][p] is the expected value of continuing if we have d dice to throw and p points.
