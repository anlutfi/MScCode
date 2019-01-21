from GameObject import GameObject

collisionassert = "Collision."

class Collision:
    "collision between two gameobjects"
    
    def __init__(self, culprit, victim, turn):
        """Collision.__init__(self, obj1, obj2)
        initialization for Collision object.
        
        culprit and victim are the two objects involved in the collision
        turn is the turn number on which the collision occured"""
    
        fassert = collisionassert + "__init__(). "
        if culprit != None:
            assert culprit.getSuperClassName() == 'GameObject', fassert + "culprit not instance of GameObject"
        if victim != None:
            assert victim.getSuperClassName() == 'GameObject', fassert + "victim not instance of GameObject"
        assert turn.__class__ == int, fassert + "invalid turn number"
        
        
        ##The first object involved in the collision
        self.culprit = culprit
        
        ##The second object involved in the collision
        self.victim = victim
        
        ##The Number of the turn in which the collision occured
        self.turn = turn
        
    def introduction(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a first introduction of the object,
        to receivers that are unaware of its existence.
        """
        return {"class": self.__class__.__name__,
                "culprit": self.culprit.objid,
                "victim": self.victim.objid,
                "turn": self.turn
               }
        
    def catchingUp(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a update on the object's state,
        sent to receivers that are already able to identify the object.
        """
        return self.introduction()
    
