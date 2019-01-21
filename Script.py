##@package Script
#File with the Script class definition

from GameObject import GameObject

scriptassert = "Script."

class Script:
    """Script to dictate behavior of a GameObject. onCreate, onUpdate, onCollision
    and onInteraction functions are called by the game's main loop.
    """
    
    def __init__(self,
                 owner,
                 onCreate = lambda x: None,
                 onUpdate = lambda x: None,
                 onCollision = lambda x, y: None,
                 onInteraction = lambda x, y: None
                ):
        """Script.__init__(self,
                      owner,
                      onCreate = lambda: None,
                      onUpdate = lambda: None,
                      onDestroy = lambda: None,
                      onCollision = lambda x: None
                     )
           Initialization function for a Script object
           
           owner is the GameObject to which the Script refers
           
           onCreate is a function that will be called when the object is created
           
           onUpdate is a function that will be called once per turn
           
           onCollision is a function that will be called when owner collides
           with another object, which is the function's argument
           
           onInteraction is a function that will be called when owner
           suffers an interaction. It must receive the object that started the
           Interaction as its argument
        """
                   
        fassert = scriptassert + "__init__(). "
        assert owner.getSuperClassName() == 'GameObject', fassert + "owner not GameObject"
        assert onCreate.__class__.__name__ == 'function', fassert + "onCreate not function"
        assert onUpdate.__class__.__name__ == 'function', fassert + "onUpdate not function"
        assert onCollision.__class__.__name__ == 'function', fassert + "onCollision not function"
        assert onInteraction.__class__.__name__ == 'function', fassert + "onInteraction not function"
        
        
        ##The GameObject which the script affects
        self.owner = owner
        owner.script = self
        
        ##Function to be called once after the instantiation of self.owner
        self.onCreate = onCreate
        
        ##Function to be called at each turn
        self.onUpdate = onUpdate
        
        ##Function to be called when self.owner collides with another GameObject
        self.onCollision = onCollision    
        
        ##function to be called when self.owner suffers an interaction.
        #It must receive the object that started the Interaction as its argument
        self.onInteraction = onInteraction         
                 
