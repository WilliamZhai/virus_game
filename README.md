# Virus Spread Simulator Game

### Description
This is a simulation game where players are settled in a closed community where a virus
is discovered. Players are told to stay home and practice social distancing until the 
virus is gone, but they must also get food from the store.

### Details
* Players have the goal to survive for as long as possible or until the game is finished.
* Every round, the surviving players must pick an action.
* Locations can contain a virus. Players that appear at a infected location have a
chance to catch the virus that is present.
* Players who carry viruses have a chance to spread the viruses they carry to the 
locations they go to.
* Once a virus is picked up by a player or is spread at a location, its infection
rate will decrease and disappear over time. 
* Players have hunger level that decreases over time, they can go to utility locations
to replenish their hunger level.

### Installation Requirements
create virtual environment:
- [virtual environment help](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)


### Instructions
from the virus_game fold run:
- pip install requirements.txt
- python src/app.py

Now you can play the game, there should be a gui pop up with information of the game.
As well you can check the stdout for information of the game state.
