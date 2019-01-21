from copy import copy
from Game import *
from Piece import *
 
INDEFL = -1

dirfunc = {leftup: (LEFT, UP),
           rightup: (RIGHT, UP), 
           leftdown: (LEFT, DOWN),
           rightdown: (RIGHT, DOWN)
          }

states = []
diffs = []

def broadCastState(game):
    states.append( game.currentState() )
    if game.turncount == 0:
        diffs.append( game.currentState() )
    else:
        diffs.append( game.currentStateDiff() )


def finit(game):
    whites = Team.getTeamByName('whites')
    blacks = Team.getTeamByName('blacks')
    
    for j in range(3):
        for i in range(4):
            ii = (i * 2 + 1 if j == 1 else i * 2)
            whites.members[i + j * 4].position = game.space.grid.g[ii][j].center()
    
    for j in range(5, 8):
        for i in range(4): 
            ii = (i * 2 + 1 if j != 6 else i * 2)
            blacks.members[i + (j - 5) * 4].position = game.space.grid.g[ii][j].center()
    
    for piece in game.gameobjects:
        if piece.script != None:
            piece.script.onCreate(piece)
            
    for team in Team.teams:
        team.updateScore()
        
    game.pushState( game.initialState() )  
    states.append(game.statebuff[0])
    
      
def fturn(game):
    whites = Team.getTeamByName('whites')
    blacks = Team.getTeamByName('blacks')
    
    #TODO end game condition
    game.collisions = []
    
    nexttoplay = (blacks if game.turncount % 2 == 0 else whites)
        
    for piece in game.gameobjects:
        piece.interactionQ = []
        if piece.team != nexttoplay:
            piece.latency = 1
        
    captureavailable = False
    availablecaptures = []
    
    
    def willCapture(move):
        p = move[0].gridposition()
        d = move[1]
        l = game.space.grid.g[ p[X] + d[X] ][ p[Y] + d[Y] ].gameobjects
        try:
            if ( l != []
                 and l[0].team != nexttoplay
                 and( LEFTEDGE <= p[X] + d[X] * 2 <= RIGHTEDGE
                      and LOWEREDGE <= p[Y] + d[Y] * 2 <= UPPEREDGE
                    )
                 and piece.space.grid.g[ p[X] + (d[X] * 2) ][ p[Y] + (d[Y] * 2) ].gameobjects == []
               ):
                return True
        except IndexError:
            pass
            
        return False
    
    
    def directions(piece):
        H = [LEFT, RIGHT]
        V = [DOWN, UP]
        p = piece.gridposition()
        directions =  [ (h, v) for h in H for v in V
                        if (
                            (  ( v == UP and p[Y] != UPPEREDGE
                                and (nexttoplay == whites
                                     or piece.tags[0] == GameObject.tagdomain['king']
                                    )
                               )
                               or ( v == DOWN and p[Y] != LOWEREDGE
                                    and (nexttoplay == blacks
                                         or piece.tags[0] == GameObject.tagdomain['king']
                                        )
                                  )
                            )
                            and( (h == LEFT and p[X] != LEFTEDGE)
                                  or (h == RIGHT and p[X] != RIGHTEDGE)
                               )
                           )
                      ]
               
        return directions
    
    
    for piece in nexttoplay.members:
        for d in directions(piece):
            print d
            if willCapture( (piece, d) ):
                print 'True'
                captureavailable = True
                availablecaptures.append( (piece, d) )
    
    
    def validMove():
        if captureavailable:
            for (piece, direction) in availablecaptures:
                for (interaction, interactor, lcond, lcons) in piece.interactionQ:
                    if dirfunc[interaction] == direction:
                        return True
        else:
            for piece in nexttoplay.members:
                for (interaction, interactor, lcond, lcons) in piece.interactionQ:
                    if interaction.fconditions(lcond):
                        return True
        
        return False
    
    
    printBoard(game.space.grid)
        
    if not captureavailable:
        while not validMove():
            getInteraction()
        
        escape = False
        for piece in nexttoplay.members:
            for (interaction, interactor, lcond, lcons) in piece.interactionQ:
                if interaction.interact(lcond, lcons):
                    piece.interactionQ = []
                    piece.script.onUpdate(piece)
                    escape = True
            if escape:
                break                
    
    while captureavailable:
        while not validMove():
            getInteraction()
        
        escape = False
        for (piece, direction) in availablecaptures:
            for (interaction, interactor, lcond, lcons) in piece.interactionQ:
                if dirfunc[interaction] == direction:
                    x = interaction.interact(lcond, lcons)
                    piece.interactionQ = []
                    captureavailable = False
                    availablecaptures = []
                    piece.script.onUpdate(piece)
                    p = piece.gridposition()
                    lp = piece.lastgridposition
                    game.space.grid.g[ lp[X] ][ lp[Y] ].removeObject(piece)
                    game.space.grid.g[ p[X] ][ p[Y] ].addObject(piece)
                    piece.lastgridposition = p
                    
                    for d in directions(piece):
                        if willCapture( (piece, d) ):
                            game.pushState(game.currentState())
                            broadCastState(game)
                            captureavailable = True
                            availablecaptures.append( (piece, d) )
                            escape = True
            
            if escape:
                break
        
        printBoard(game.space.grid)
    
    for piece in Layer.getLayerByName('active').objects:
        if piece.script != None:
            piece.script.onUpdate(piece)
        
    for team in Team.teams:
        team.updateScore()
    
    broadCastState(game)

    
def fend(game):
    whites = Team.getTeamByName('whites')
    blacks = Team.getTeamByName('blacks')
    
    return ( whites.name if whites.score > blacks.score 
                         else (blacks.name if blacks.score > whites.score
                               else 'tie'
                              )
           )


class Checkers(Game):
    
    def __init__(self, cstatebuffsize):
        board = GameSpace(0.0, 8.0,#x
                          0.0, 8.0,#y
                          0.0, 0.0,#z
                          cellsize = 1.0
                         )

        GameObject.initTagDomain( {'man': 0, 'king': 1} )
 
        whites = Team(1, 'whites', [])
        blacks = Team(2, 'blacks', [])

        active = Layer('active', [])
        inactive = Layer('inactive', [])
 
        for i in range(24):
            Piece(i,
                  board.origin,
                  board,
                  (0.0,0.0,0.0),
                  (1.0,1.0,1.0),
                  (0.0,0.0,0.0),
                  [ GameObject.tagdomain['man'] ],[],[],
                  ([leftup.interactionid, rightup.interactionid] if i < 12
                   else [leftdown.interactionid, rightdown.interactionid]
                  ),
                  layer = active,
                  team = (whites if i < 12 else blacks)
                 )
        
        for piece in Piece.pieces:
            piece.script =  piecebehavior(piece) 
 
        Game.__init__(self,
                      'Checkers',
                      "Simple Checkers game with brittish rules",
                      board,
                      Piece.pieces,
                      Team.teams,
                      True,
                      [],
                      finit = finit,
                      fturn = fturn,
                      fend = fend,
                      statebuffsize = cstatebuffsize
                     )
                     
                     
import sys

def printBoard(grid):
    whites = Team.getTeamByName('whites')
    blacks = Team.getTeamByName('blacks')
    g = grid.g    
    
    print "      0      1      2      3      4      5      6      7"
    for y in range(7, -1, -1):
        print "   +------+------+------+------+------+------+------+------+"
        print "   |      |      |      |      |      |      |      |      |"
        sys.stdout.write(" " + str(y) + " ")
                
        for x in range(8):
            cell = g[x][y]
            if cell.gameobjects == []:
                sys.stdout.write("|      ")
            else:
                piece = cell.gameobjects[0]
                objid = piece.objid % 12
                sys.stdout.write( "| " + ('B' if piece.team == blacks else 'W')
                                  + hex(objid)[-1]
                                  + ("   " if piece.tags[0] == 0 else "K  ")
                                )
        print "| "+ str(y) +"\n   |      |      |      |      |      |      |      |      |"
    
    print "   +------+------+------+------+------+------+------+------+"
    print "      0      1      2      3      4      5      6      7"  

def getInteraction():
    commint = {"lu": leftup,
               "ru": rightup,
               "ld": leftdown,
               "rd": rightdown, 
               "ul": leftup,
               "ur": rightup,
               "dl": leftdown,
               "dr": rightdown
              }
    
    command = raw_input("move: ")
    objid = ( int(command[1], 16) if command[0] == 'w' else int(command[1], 16) + 12 )
    piece = GameObject.objFromId(objid)
    piece.addInteraction(commint[ command[2:] ], None, piece, piece)
                  

    
     
     
     
     
 
 
 
 
        

