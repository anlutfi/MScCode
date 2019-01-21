def finit(game):
    for gameobj in game.gameobjects:
        if gameobj.script != None:
            gameobj.script.onCreate(gameobj)
            
            if game.isdiscrete:
                p = gameobj.gridposition()
                gameobj.lastgridposition = p
                game.space.grid.g[ p[X] ][ p[Y] ].addObject(gameobj)
    
    for team in Team.teams:
        team.updateScore()
        
    #Check for initial collisions
    #Check for initial interactions
    
    game.pushState( game.initialState() )
                

def fturn(game):
    if False: #replace for endgame condition
        game.lastturn = True
        #return here depending on implementation choices
        
    #Insert Interaction computing here
    
    #Insert collision detection here
    
    for collision in game.collisions:
        collision.culprit.script.onCollision(collision.culprit,
                                             collision.victim
                                            )
        collision.victim.script.onCollision(collision.culprit,
                                            collision.victim
                                           )
        game.collisions.remove(collision)
        #add extra collision treatment here
        
        
    for poll in game.polls:
        pass #replace for poll treatment
        
    for gameobj in game.gameobjects:
        if gameobj.script != None:
            gameobj.script.onUpdate(gameobj)
            
        p = gameobj.gridposition()
        if p != gameobj.lastgridposition:
            lp = gameobj.lastgridposition
            game.space.grid.g[ lp[x] ][ lp[y] ].removeObject(gameobj)
            game.space.grid.g[ p[x] ][ p[y] ].addObject(gameobj)
            gameobj.lastgridposition = p
            
    for team in Team.teams:
        team.updateScore()
        
    game.pushState( game.currentState() )

def fend(game):
    pass #replace for endgame
