# Color Fill Game
### Game Description
Upon startup, the user is presented with a board of size 20 by 10. Each cell in the board is filled by one of the four available colors. 
The objective of the game is to have the board be filled with a single color. On each turn, the user is prompted to choose one of the four colors. 
Upon a choice, the board will then be colored with that color from the top left corner in a flood fill manner. For example, given the board\
`R R B`\
`G R R`\
`B B R`\
If the user decides to play the move `G`, then the resulting board will be\
`G G B`\
`G G G`\
`B B G`\
The user is allowed 21 moves before the game is over.
At each turn, the user has the ability to toggle on 'Knight Mode'. This changes
the fill method to be from immediately adjacent neighbors to neighbors found using the 
chess piece Knight's movement. Using the original example from above, playing the move `G` would result in the board\
`G R B`\
`G R G`\
`B B R`\
Additionally, the user is able to request a hint from the AI agent before any turn in the game.

### Command Line Usage
Running the command `python game.py` with no additional arguments will allow
the user to play the game through the graphical user interface (GUI). 
