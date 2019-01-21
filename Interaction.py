##@package Interaction
#File with Interaction class

interactionassert = "Interaction."
class Interaction:
    """A class that treats the interaction between players and other GameObjects
    Basically its a set of conditions and one of consequences. When the conditions
    are met, the consequences happen
    """
    
    ##Static List of all interactions
    interactions = []
    
    def __init__(self, interactionid, fconditions, fconsequences):
        """Interaction.__init__(self, interactiontype, fconditions, fconsequeces)
        Initialization function for an Interaction object
        
        interactiontype is the type of the interaction.
        interactiontype MUST be in Interaction.possibletypes.
        
        fconditions is a boolean function that returns True when the interaction occurs
        
        fconsequences is a function that computes the consequences of the interaction
        
        In short, when fconditions returns True, fconsequences is called
        """
        
        fassert = interactionassert + "__init__(). "
        assert interactionid not in [i.interactionid for i in Interaction.interactions], fassert + "interactionid not unique"
        assert fconditions.__class__.__name__ == 'function', fassert + "fconditions not a function"
        assert fconsequences.__class__.__name__ == 'function', fassert + "fconsequences not a function"
        
        ##The interaction's type.
        #One of the possible types in Interaction.possibletypes
        self.interactionid = interactionid
        
        ##Boolean function that returns True for when the consequences are met
        # and False when not
        self.fconditions = fconditions
        
        ##Function to be called when the return value of self.fconditions is True
        self.fconsequences = fconsequences
        
        Interaction.interactions.append(self)
        
    
    def interact(self, lcond, lcons):
        """Interaction.interact(self, lcond, lcons)
        
        Function that checks if the conditions are meant and, if so, executes the interaction
        
        lcond is a parameter list to be passed to self.fconditions
        lcons is a parameter list to be passed to self.fconsequences
        """
        
        if self.fconditions(lcond):
            return self.fconsequences(lcons)
        return False
            
    def introduction(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a first introduction of the object,
        to receivers that are unaware of its existence.
        """
        return {"class": self.__class__.__name__,
                "interactionid": self.interactionid
               }
    
    def catchingUp(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a update on the object's state,
        sent to receivers that are already able to identify the object.
        """
        return self.introduction()
        
    @staticmethod    
    def getInteractionById(interactionid):
        for interaction in Interaction.interactions:
            if interaction.interactionid == interactionid:
                return interaction
        return None
