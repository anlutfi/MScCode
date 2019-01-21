from Interaction import Interaction
from Space import X, Y
from GameObject import GameObject
from Collision import Collision

LEFT = DOWN = -1
RIGHT = UP = 1

RIGHTEDGE = UPPEREDGE = 7
LEFTEDGE = LOWEREDGE = 0

def capture(culprit, victim):
    culprit.score += 1
    victim.script.onCollision(victim)


def isMoveClear(piece, direction):
    if direction[X] == 0 or direction[Y] == 0:
        return
    
    direction = ( direction[X]/abs(direction[X]),
                  direction[Y]/abs(direction[Y])
                )

    p = piece.gridposition()
    if ( (p[X] == RIGHTEDGE and direction[X] == RIGHT)
         or (p[X] == LEFTEDGE and direction[X] == LEFT)
         or (p[Y] == UPPEREDGE and direction[Y] == UP)
         or (p[Y] == LOWEREDGE and direction[Y] == DOWN)
       ): #if trying to move out of board
        return False
         
    
    l = piece.space.grid.g[ p[X] + direction[X] ][ p[Y] + direction[Y] ].gameobjects
    if (l != []
        and( ( (p[X] + direction[X] * 2 < LEFTEDGE
                or p[X] + direction[X] * 2 > RIGHTEDGE
               )
               or(p[Y] + direction[Y] * 2 < LOWEREDGE
                  or p[Y] + direction[Y] * 2 > RIGHTEDGE
                 )
             )
             or( l[0].team == piece.team #if next cell contains a piece of the same color
                 or (piece.space.grid.g[ p[X] + direction[X] * 2 ]
                                       [ p[Y] + direction[Y] * 2 ].gameobjects != []
                    ) #or if the second next cell is not empty
               )
           )
        
       ):
        return False
    else: #if next cell is empty or a rival piece and capture is possible
        return True


def move(piece, direction):
    if direction[X] == 0 or direction[Y] == 0:
        return
    
    direction = ( direction[X] / abs(direction[X]),
                  direction[Y] / abs(direction[Y])
                )
    
    p = piece.gridposition()
    l = piece.space.grid.g[ p[X] + direction[X] ][ p[Y] + direction[Y] ].gameobjects
    if l == []: #if next cell is clear
        piece.position = ( piece.space.grid.g[ p[X] + direction[X] ]
                                             [ p[Y] + direction[Y] ].center()
                         )
    else: #if a capture is going to occur 
        piece.position = ( piece.space.grid.g[ p[X] + direction[X] * 2 ]
                                             [ p[Y] + direction[Y] * 2 ].center()
                         )#move piece
        capture(piece, l[0])

cond = lambda direction: lambda piece:
                         isMoveClear(piece, direction)
cons = lambda direction: lambda piece:
                         move(piece, direction)

leftup = Interaction(  1, cond( (LEFT, UP) ),
		       cons( (LEFT, UP) )  )
rightup = Interaction(  2, cond( (RIGHT, UP) ), cons( (RIGHT, UP) )  )
leftdown = Interaction(  3, cond( (LEFT, DOWN) ), cons( (LEFT, DOWN) )  )
rightdown = Interaction(  4, cond( (RIGHT, DOWN) ), cons( (RIGHT, DOWN) )  )
