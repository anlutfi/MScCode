from GameObject import GameObject
from piecebehavior import *
from pieceinteractions import *

class Piece(GameObject):
    
    pieces = GameObject.gameobjects
    
    def __init__(self,
                 objid,
                 position,
                 space,
                 rotation,
                 scale,
                 lookat,
                 tags,
                 visibility,
                 interactability,
                 interactiondomain,
                 isrigid = False,
                 parent = None,
                 layer = None,
                 interactiontimelimit = 0,
                 script = None,
                 team = None,
                 latency  = 0,
                 score = 0
                ):
        GameObject.__init__(self,
                            objid,
                            position,
                            space,
                            rotation,
                            scale,
                            lookat,
                            tags,
                            visibility,
                            interactability,
                            interactiondomain,
                            isrigid,
                            parent,
                            layer,
                            interactiontimelimit,
                            script,
                            team,
                            latency,
                            score
                           )

    def promotion(self):
        self.tags = [ GameObject.tagdomain['king'] ]
        self.interactiondomain = [leftup.interactionid,
                                  rightup.interactionid,
                                  leftdown.interactionid,
                                  rightdown.interactionid
                                 ]




































