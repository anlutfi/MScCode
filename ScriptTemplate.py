def onCreate(gameobject):
    pass #replace for initialization
    
def onCollision(gameobject, collision):
    pass #replace
    
def onInteraction(gameobject, interaction):
    gameobject.addInteraction(interaction)
    
def onUpdate(gameobject):
    if gameobject.latency != 0:
        for interaction in interactionQ:
            lcond = []#replace for parameter list for interaction.interact()
            lcons = []#replace for parameter list for interaction.interact()
            interaction.interact(lcond, lcons)
            interactionQ.remove(interaction)
            
    gameobject.latency = max(gameobject.latency - 1, 0)        
    #add more
