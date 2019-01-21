##@package Character
#File with Character class definition

from GameObject import *

class Character(GameObject):
    """A GameObject that can move in space and have a behaviour. player or NPC"""
    def __init__(self,
                 objid,
                 position,
                 gridposition,
                 rotation,
                 scale,
                 lookat,
                 tags,
                 visibility,
                 interactability,
                 interactiondomain,
                 
                 v0,
                 a0,
                                  
                 isrigid = False,
                 parent = None,
                 layer = None,
                 interactiontimelimit = 0,
                 script = None,
                 team = None,
                 latency  = 0,
                 score = 0
                ):
        """Character.__init__(self,
                 objid,
                 position,
                 gridposition,
                 rotation,
                 scale,
                 lookat,
                 tags,
                 visibility,
                 interactability,
                 interactiondomain,
                 
                 v0,
                 a0,
                                  
                 isrigid = False,
                 parent = None,
                 layer = None,
                 interactiontimelimit = 0,
                 script = None,
                 team = None,
                 latency  = 0,
                 score = 0
                )
        Initialization function for a Character. All arguments except v0 and a0
        are documented on GameObject class
        
        v0 is a 3D vector of the object's initial velocity
        a0 is a 3D vector of the object's initial acceleration
        """
        
        GameObject.__init__(self,
                            objid,
                            layer,
                            tag,
                            visibility,
                            interactability,
                            position,
                            rotation,
                            scale,
                            lookat,
                            isrigid,
                            interactiondomain,
                            fprocessinteraction,
                            interactiontimelimit,
                            fupdate,
                            team = team,
                            latency = latency
                           )
        
        assert v0.__class__ == numpy.ndarray, fassert + "v0 not numpy.ndarray"
        assert a0.__class__ == numpy.ndarray, fassert + "a0 not numpy.ndarray"
        
        ##A 3D vector for the Character's velocity
        self.velocity = v0
        
        ##A 3D vector for the Character's acceleration
        self.acceleration = a0 
        
    def introduction(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a first introduction of the object,
        to receivers that are unaware of its existence.
        """
        return {"class": self.__class__.__name__,
                "parent obj": GameObject.introduction(self),
                "velocity": self.velocity,
                "acceleration": self.acceleration
               }
                
    
    def catchingUp(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a update on the object's state,
        sent to receivers that are already able to identify the object.
        """
        return {"class": self.__class__.__name__,
                "parent obj": GameObject.catchingUp(self),
                "velocity": self.velocity,
                "acceleration": self.acceleration
               }
       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
