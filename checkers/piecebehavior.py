from Script import Script
from Space import X, Y
from GameObject import Layer, GameObject

BLACKEDGE = 7
WHITEEDGE = 0

INDEFL = -1

def onCreate(piece):
    gp = piece.gridposition()
    piece.position = piece.space.grid.g[ gp[X] ][ gp[Y] ].center()
    piece.lastgridposition = gp
    GameObject.game.space.grid.g[ gp[X] ][ gp[Y] ].addObject(piece)
    

def onCollision(piece):
    piece.position = (-1, -1, -1)
    piece.latency = INDEFL
    piece.layer.removeObject(piece)
    piece.layer = Layer.getLayerByName('inactive')
    piece.layer.addObject(piece)
    lp = piece.lastgridposition
    piece.space.grid.g[ lp[X] ][ lp[Y] ].removeObject(piece)
    

def onUpdate(piece):
    if piece.latency != 0:
        for (interaction, interactor, lcond, lcons) in piece.interactionQ:
            interaction.interact(lcond, lcons)
            interactionQ.remove(interaction)
        
        gp = piece.gridposition()
        piece.position = piece.space.grid.g[ gp[X] ][ gp[Y] ].center()
        if ( (piece.gridposition()[Y] == WHITEEDGE
              and piece.team.name == 'blacks'
             )
             or (piece.gridposition()[Y] == BLACKEDGE
                 and piece.team.name == 'whites'
                )
           ):
            piece.promotion()
    
    piece.latency = ( max(piece.latency - 1, 0) if piece.latency != -1 else -1 )
    
    p = piece.gridposition()
    lp = piece.lastgridposition
    if p != lp:
        GameObject.game.space.grid.g[ lp[X] ][ lp[Y] ].removeObject(piece)
        GameObject.game.space.grid.g[ p[X] ][ p[Y] ].addObject(piece)
        piece.lastgridposition = p

def onInteraction(piece, interaction):
    if interaction.interactionid in piece.interactiondomain:
        piece.addInteraction(interaction, None, piece, piece)
        return True
    return False
    
piecebehavior = lambda owner: Script(owner,
                                     onCreate,
                                     onUpdate,
                                     onCollision,
                                     onInteraction
                                    )
