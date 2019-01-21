##@package GameObject
#File containing Layer and GameObject class definitions


from Team import Team
from Interaction import Interaction
import numpy

layerassert = "Layer."
class Layer:
    """A layer is a set of GameObjects. 
    Grouping objects in layers can save CPU time
    """
    
    ##The list of Layers
    layers = []
    
    def __init__(self, layername, initialobjects):
        """Layer.__init__(self, layername, objects)
        Initialization funciton.
        
        layername is the Layer's name
        
        initialobjects is a list of GameObjects that belong to the Layer
        """
        
        fassert = layerassert + "__init__(). "
        for l in Layer.layers:
            assert l.layername != layername, fassert + "Repeated layer name."
            for obj in initialobjects:
                assert obj not in l.objects, fassert + "object already in a layer"
        
        ##The Layer's name
        self.layername = layername
        
        ##A list of the GameObjects in the Layer
        self.objects = initialobjects
        for obj in self.objects:
            obj.layer = self
        
        Layer.layers.append(self)
        
    
    def addObject(self, obj):
        """Layer.addObject(self, obj)
        A function that adds a GameObject obj to a Layer
        
        Returns True if the object is successfully added and False otherwise
        """
        
        fassert = layerassert + "addObject(). "
        assert obj.getSuperClassName() == 'GameObject', fassert + "obj not a GameObject"
        
        for l in Layer.layers:
            if obj in l.objects:
                return False
        
        self.objects.append(obj)
        obj.layer = self
        return True

   
    def removeObject(self, obj):
        """Layer.removeObject(self, obj)
        A function that removes a GameObject obj from a Layer
        """
        fassert = layerassert + "removeObject(). "
        assert obj.getSuperClassName() == 'GameObject', "obj not a GameObject"
        
        try:
            self.objects.remove(obj)
            obj.layer = None
            return True        
        except ValueError: #object not in list
            return False
            
    @staticmethod
    def getLayerByName(layername):
        """Layer.getLayerByName(layername) [STATIC]
        Returns a Layer object given its name layername.
        Returns None if there's no layer by that name
        """
        
        for l in Layer.layers:
            if l.layername == layername:
                return l
        return None
        
    def introduction(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a first introduction of the object,
        to receivers that are unaware of its existence.
        """
        return {"class": self.__class__.__name__,
                "layername": self.layername,
                "objects": [obj.objid for obj in self.objects]
               }
        
    def catchingUp(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a update on the object's state,
        sent to receivers that are already able to identify the object.
        """
        return self.introduction()
        
        

gameobjectassert = "GameObject."
class GameObject:
    """A class that represents all objects in a game.
    To be inherited by more specific classes
    """
    
    ##A list of every GameObject in play
    gameobjects = []
    
    ##A dictionary of all possible tags for GameObjects.
    #Each GameObject can have any number of tags (self.tags)
    tagdomain = {}
    
    ##A reference to an instance of class Game.
    game = None
    
    @staticmethod
    def initTagDomain(tagdomain):
        """GameObject.initTagDomain(tagdomain) [STATIC]
        Function to initialize GameObject.tagdomain with a dictionary tagdomain
        """
        
        fassert = gameobjectassert + "initTagDomain(). "
        assert tagdomain.__class__ == dict, fassert + "parameter not a dictionary"
        
        GameObject.tagdomain = tagdomain
        
    
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
        """GameObject.__init__(self,
                      objid,
                      parent,
                      layer,
                      tags,
                      visibility,
                      interactability,
                      position,
                      space,
                      rotation,
                      scale,
                      lookat,
                      isrigid,
                      interactiondomain,
                      fprocessinteraction,
                      interactiontimelimit,
                      script,
                      team = None,
                      latency  = 0,
                      score = 0
                     )
           Initialization function for a GameObject.
           
           objid is the identification number
           
           position is a 3d vector indicating the object's position
           
           space is a GameSpace object to which the GameObject's spatial information refers
                      
           rotation is a 3d vector indicating the object's rotation
           
           scale is a 3d vector indicating the object's scale relative to its
           original size
           
           lookat is a 3d vector indicating the direction
           to which the object is looking
           
           isrigid is a boolean to prevent objects from going through each other
           
           parent is a parent GameObject to be used in the scene graph
           at the studio. position, rotation and scale will be relative to parent.
           
           layer is the game layer to which the object belongs
           
           tags are a subset of GameObject.tagdomain
           
           visibility is a list intended to contain everyone who can see the object
           
           interactability is a list intended to contain everyone
           who can interact with the object
           
           interactiondomain is a list of possible interactions for the object.
           
           interactiontimelimit is the time limit a player has to interact with
           the object at each turn
           
           script is a Script Object who will dictate the object's
           behavior at each turn
           
           team is a Team object that indicates to which team the object belongs

           latency is the number of turns the object will be inactive.
           -1 is indefinitely
           
           score is the GameObject's score in the game.
           
        """
           
        #TODO asserts
        fassert = gameobjectassert + "__init__(). "
        assert objid.__class__ == int, fassert + "objid not int"
        assert (objid not in [obj.objid for obj in GameObject.gameobjects]), fassert + "repeated objid"
        if parent != None:
            assert parent.getSuperClassName() == 'GameObject', fassert + "parent not a GameObject"
        
        if layer != None:
            assert layer in Layer.layers, fassert + "invalid layer"
        
        tagvalues = GameObject.tagdomain.values()
        for tag in tags:
            assert tag in tagvalues, fassert + "tag not in GameObject.tagdomain"
            
        assert visibility.__class__ == list, fassert + "visibility is not a list"
        assert interactability.__class__ == list, fassert + "interactability is not a list"
        
        #assert position.__class__ == numpy.ndarray, fassert + "position not numpy.ndarray"
        #assert rotation.__class__ == numpy.ndarray, fassert + "rotation not numpy.ndarray"
        #assert scale.__class__ == numpy.ndarray, fassert + "scale not numpy.ndarray"
        #assert lookat.__class__ == numpy.ndarray, fassert + "lookat not numpy.ndarray"
        
        assert isrigid.__class__ == bool, fassert + "isrigid not boolean"
        
        for iid in interactiondomain:
            assert Interaction.getInteractionById(iid) != None, "interactiondomain contain an invalid member"
        
        assert interactiontimelimit.__class__ == int, fassert + "interactiontimelimit not int"
        if script != None:
            assert script.__class__.__name__ == 'Script', fassert + "script not from class Script"
        if team != None:
            assert team.__class__.__name__ == 'Team', fassert + "team not from class Team"
    
        assert latency.__class__ == int and latency >= -1, fassert + "invalid latency"
        assert score.__class__ == int, fassert + "score not int"
                 
        ##A GameObject's unique identifier.
        self.objid = objid
        
        ##A GameObject's parent. It must be another GameObject or None
        self.parent = parent
        
        ##The Layer to which the GameObject belongs
        self.layer = layer
        if self.layer != None:
            self.layer.addObject(self)
        
        ##A list of tags (a subset of GameObject.tagdomain)
        self.tags = tags
        
        ##A list of GameObjects allowed to see the GameObject
        #Implementation of visibility is left to the game developer
        self.visibility = visibility
        
        ##A list of GameObjects allowed to interact with the GameObject
        #Implementation of interactability is left to the game developer
        self.interactability = interactability
        
        ##A 3D vector with the GameObject's spacial position
        #relative to self.parent
        self.position = position
        
        ##A GameSpace object to which all of the GameObject spatial information
        #refers
        self.space = space
        
        ##A 2D vector with the coordinates of the GameSpace.grid's cell in which
        #the GameObject is
        self.gridposition = lambda: self.space.grid.getGridPosition(self.position)
        
        ##A 2D vector with the coordinates of the GameSpace.grid's cell in which
        #the GameObject was one turn before the current turn.
        self.lastgridposition = None
        
        ##A 3D vector with the GameObject's rotation relative to self.parent
        self.rotation = rotation
        
        ##A 3D vector with the GameObject's scale relative to self.parent
        self.scale = scale
        
        ##A 3D vector with the direction at which the GameObject is looking
        self.lookat = lookat
        
        ##A bool that indicates if the GameObject is rigid and,
        #therefore, subject to collisions
        self.isrigid = isrigid
        
        ##A list of possible interaction types (Intreraction,interactiontype) for the GameObject.
        self.interactiondomain = interactiondomain
        
        ##A time limit in which another object must interact with the GameObject
        #in a turn
        self.interactiontimelimit = interactiontimelimit
        
        ##A queue of Interactions yet to be processed
        self.interactionQ = []
        
        ##A Script object to dictate the GameObject's behaviour
        self.script = script
        if self.script != None:
            self.script.owner = self
        
        ##The GameObject's score in the game
        self.score = score
        
        ##The Team to which the GameObject belongs
        self.team = team
        if self.team != None:
            self.team.addMember(self)
        
        ##The number of turns the GameObject must remain inactive
        #-1 indicates an indefinite latency
        self.latency = latency
        
        GameObject.gameobjects.append(self)
        
    def addInteraction(self, interaction, interactor, lcond, lcons):
        """GameObject.addInteraction(self, interaction, interactor, lcond, lcons)
        Checks if an Interaction which a GameObject suffered is valid.
        If so, it adds the Interaction to the GameObject's interactionQ
        
        interaction is an object of class Interaction
        
        interactor is the GameObject -usually a Player- that made the Interaction
        
        lcond is a list of parameters to be passed to interaction.fconditions
        
        lcons is a list of parameters to be passed to interactions.fconsequences
        if interaction.fconditions(lcond) returns True
        """
        
        fassert = gameobjectassert + "addInteraction(). "
        assert interaction.__class__.__name__ == "Interaction", fassert + "interaction not an instance of Interaction"
        
        if (self.latency != 0
            or interaction.interactionid not in self.interactiondomain
           ):
            return False
        else:
            self.interactionQ.append( (interaction, interactor, lcond, lcons) )
            return True
        
    def addTags(self, tagkeys):
        """GameObject.addTag(self, tagkeys)
        adds a list of tags to GameObject.tags.
        Each element in the argument tags is a key for GameObject.tagdomain, NOT A VALUE.
        if one of the tags is not in GameObject.tagdomain, it is not added
        """
        for key in tagkeys:
            if ( key in GameObject.tagdomain.keys()
                 and GameObject.tagdomain[key] not in self.tags
               ):
                self.tags.append(GameObject.tagdomain[key])
        
    def removeTags(self, tagkeys):
        """GameObject.removeTags(self, tagkeys)
        removes a list of tags from a GameObject's tags attribute.
        Each element in the argument tagkeys is a key for GameObject.tagdomain, NOT A VALUE.
        If a tag in tagkeys is not in the GameObject's tags list, it's ignored
        """
        for key in tagkeys:
            if (key in GameObject.tagdomain.keys()
                and GameObject.tagdomain[key] in self.tags
               ):
                self.tags.remove(GameObject.tagdomain[key])
    
    def getSuperClassName(self):
        """A function that returns 'GameObject'.
        Used to assert that the supermost class of an object is GameObject"""
        return GameObject.__name__
        
    
    def introduction(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a first introduction of the object,
        to receivers that are unaware of its existence.
        """ 
        return {"class": self.__class__.__name__,
                "objid": self.objid,
                "parent": None if self.parent == None else self.parent.objid,
                "layer": None if self.layer == None else self.layer.layername,
                "tags": list(self.tags),
                "visibility": list(self.visibility),
                "interactability": list(self.interactability),
                "position": self.position,
                "gridposition": self.gridposition(),
                "lastgridposition": self.lastgridposition,
                "rotation": self.rotation,
                "scale": self.scale,
                "lookat": self.lookat,
                "isrigid": self.isrigid,
                "interactiondomain": list(self.interactiondomain),
                "interactiontimelimit": self.interactiontimelimit,
                "team": None if self.team == None else self.team.teamid,
                "latency": self.latency,
                "score": self.score
               }
    
    def catchingUp(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a update on the object's state,
        sent to receivers that are already able to identify the object.
        """
        return self.introduction()
    
    @staticmethod
    def objFromId(objid):
        """GameObject.objFromId(objid) [STATIC]
        Function that returns a GameObject from his objid or
        None if there`s no object by objid
        """
        for obj in GameObject.gameobjects:
            if obj.objid == objid:
                return obj
        return None
        
        
    @staticmethod
    def idFromObj(objct):
        """GameObject.idFromObj(objct) [STATIC]
        Function that retrieves a GameObject objct's objid
        if objct is in GameObject.gameobjects
        """
        for obj in GameObject.gameobjects:
            if obj == objct:
                return obj.objid
        return None
        
    
           
       
           
           
                 


