from Collision import Collision
from Space import *
from Character import *
from Script import Script

idwords = ['teamid', 'objid', 'layername']

gameassert = "Game."
class Game:
    """The Class that contains the game itself.
    It has the game's state and is responsible for its execution
    """
    
    ##The dictionary containing the Game's initial state information
    initialstate = None
    
    def __init__(self,
                 name,
                 description,
                 space,
                 gameobjects,
                 teams,
                 isdiscrete,
                 polls,
                 finit = lambda x: None,
                 fturn = lambda x: None,
                 fend = lambda x: None,
                 statebuffsize = 2
                ):
        """Game.__init__(self,
                      name,
                      description,
                      gameobjects,
                      teams,
                      
                      finit = lambda: None,
                      fturn = lambda: None,
                      fend = lambda: None,
                      statebuffsize = 2
                     )
                     
        name is the Game's name
        
        description is a brief Game description
        
        space is the Game's GameSpace
        
        gameobjects is a list of the Game's GameObjects
        
        teams is a list of the Game's Teams
        
        isdiscrete indicates if the game space is discrete.
        If so, all objects will be positioned according to space's Grid Cells
        
        finit is a function to be called once
        
        fturn is a function that marks de division between Game turns
        
        fend is a function to be called once right before the Game ends
        
        statebuffsize is the size of the states buffer, or how many turns previous
        to current are stored
        """
        
        fassert = gameassert + "__init__(). "
        assert name.__class__ == str, fassert + "name not str"
        assert description.__class__ == str, fassert + "description not str"
        assert space.__class__.__name__ == 'GameSpace', fassert + "space not instance of GameSpace"
        for obj in gameobjects:
            assert obj.getSuperClassName() == 'GameObject', fassert + "gameobjects contains instances of classes other than GameObject"
                   
        for team in teams:
            assert team.__class__.__name__ == 'Team', fassert + "teams contains instances of classes other than Team"
                   
        assert isdiscrete.__class__ == bool, fassert + "isdiscrete not bool"
        
        for poll in polls:
            assert poll.__class__.__name__ == 'Poll', fassert + "polls contains instances of classes other than Poll"
        
        assert finit.__class__.__name__ == 'function', fassert + "finit not a function"
        assert fturn.__class__.__name__ == 'function', fassert + "fturn not a function"
        assert fend.__class__.__name__ == 'function', fassert + "fend not a function"
        
        assert statebuffsize.__class__ == int, fasser + "statebuffsize not integer"
        
        
        ##The Game's name
        self.name = name
        
        ##The Game's description
        self.description = description
        
        ##Game's GameSpace object
        self.space = space
        
        ##The Game's list of GameObjects (GameObject)
        self.gameobjects = gameobjects
        
        ##The Game's list of Teams (Team)
        self.teams = teams
        
        ##Boolean to indicate whether or not the to use self.space.grid for objects position
        self.isdiscrete = isdiscrete
        
        ##A list of Polls (Poll)
        self.polls = polls
        
        ##The subset of active Polls (Poll) within self.polls
        self.activepolls = [poll for poll in self.polls if poll.isactive]

        ##The Game's initialization function
        self.finit = finit
        
        ##A function to be called on each new turn
        self.fturn = fturn
        
        ##A function to be called when the game ends
        self.fend = fend
        
        ##A boolean that inidicates if the Game's current turn is its last
        self.lastturn = False
        
        ##The number of the current turn
        self.turncount = 0
        
        ##A subset of rigid GameObjects (GameObject) within self.gameobjects
        self.rigidobjects = [obj for obj in self.gameobjects if obj.isrigid]
        
        ##A list of collisions (Collision) to be addressed
        self.collisions = []
        
        ##A list of past game states self.paststates[0] is the current state
        #self.paststates[n] is the n'th past state
        self.statebuff = [{} for i in range(statebuffsize)]
        
                
    def run(self):
        """Game.run(self)
        the Game's execution function
        """
        
        GameObject.game = self
        self.finit(self)
        self.pushState( self.initialState() )
        
        while not self.lastturn:
            self.fturn(self)
            self.turncount += 1
            self.pushState( self.currentState() )
            #broadcast state
        
        self.fend(self)
        
    
    def addPoll(self, poll):
        """Game.addPoll(self, poll)
        A function to add a Poll to a Game.
        Returns True on success and False on failure
        """ 
        
        fassert = gameassert + "addPoll(). "
        assert poll.__class__.__name__ == 'Poll', fassert + "poll is not an instance of Poll"
        
        if poll not in self.polls:
            self.polls.append(poll)
            if poll.isactive:
                self.activepolls.append(poll)
            return True
        return False
        
                
    def switchOffPoll(self, poll):
        """Game.switchOffPoll(self, poll)
        Function to make an active Poll inactive.
        Returns True on success and False on failure
        """
        
        fassert = gameasssert + "switchOffPoll(). "
        assert poll.__class__.__name__ == 'Poll', fassert + "poll is not an instance of Poll"
        
        if poll in self.activepolls:
            poll.isactive = False
            self.activepolls.remove(poll)
            return True
        return False
            
    
    def switchOnPoll(self, poll):
        """Game.switchOnPoll(self, poll)
        Function to make an inactive Poll active.
        Returns True on success and False on failure
        """
        fassert = gameasssert + "switchOnPoll(). "
        assert poll.__class__.__name__ == 'Poll', fassert + "poll is not an instance of Poll"
        
        if poll in self.polls and poll not in self.activepolls:
            poll.isactive = True
            self.activepolls.append(poll)
            return True
        return False
    
    
    def initialState(self):
        """Game.initialState(self)
        Returns a dictionary containg the game initial state
        and sets static Game.initialstate
        """
        initialstate = {"class": self.__class__.__name__,
                        "name": self.name,
                        "description": self.description,
                        "space": self.space.introduction(),
                        "gameobjects": [obj.introduction()
                                        for obj in self.gameobjects
                                       ],
                        "teams": [team.introduction()
                                  for team in self.teams
                                 ],
                        "isdiscrete": self.isdiscrete,
                        "polls": [poll.introduction()
                                  for poll in self.polls
                                 ],
                        "lastturn": self.lastturn,
                        "turncount": self.turncount
                       }
        return initialstate
    
    def currentState(self):
        """Game.currentState(self)
        Returns a dictionary containing the Game's current state
        """
        r = {"class": self.__class__.__name__,
             "name": self.name,
             "description": self.description,
             "space": self.space.catchingUp(),
             "gameobjects": [obj.catchingUp() for obj in self.gameobjects],
             "teams": [team.catchingUp() for team in self.teams],
             "isdiscrete": self.isdiscrete,
             "polls": [poll.catchingUp() for poll in self.polls],
             "lastturn": self.lastturn,
             "turncount": self.turncount
            }
        return r
    
    def pushState(self, state):
        """Game.pushState(self)
        adds the argument to self.statebuff
        """
        self.statebuff = [state] + self.statebuff[:len(self.statebuff) - 1]
    
    def currentStateDiff(self, i = 0, j = 1):
        """Game.currentStateDiff(self)
        Returns a minimal dictionary containing only the differences between
        self.statebuff[i] and self.statebuff[j]. Any object with access to the Game's
        last state can deduce its current state by the differences.
        This function is used to minimize the network's communication
        overhead.
        """        
        def diff(new, old):
            if new != old:
                if new.__class__ == dict:
                    l = []
                    for key in new.keys():
                        if ( key.__class__ == str
                             and key in idwords
                           ):
                            l.append( (key,new[key]) )
                        elif new[key] != old[key]:
                            l.append(  ( key, diff(new[key], old[key]) )  )
                    return dict(l)
             
                elif new.__class__ == list:
                    l = []
                    if len(new) != len(old):
                        l += new
                    else:
                        for i in range( len(new) ):
                            d = diff(new[i], old[i])
                            if d != None:
                                l.append(d)
                    return l 
                
                else:
                    if new != old:
                        return new                
        
        return diff(self.statebuff[i], self.statebuff[j])
        
            
            
pollassert = "Poll."
ANSWER = 0
OBJECT = 1
VOTES = 2
INDEF = -1

class Poll:
    """A class that represents a poll.
    It has a question, a list of possible answers
    and the means to compute votes to these answers"""
    
    def __init__(self, question, answersobjs, turns = INDEF, isactive = True,
                 fformat = lambda x: None
                ):
        """Poll.__init__(self, question, answersobjs, turns = INDEF, isactive = True,
                 fformat = lambda x: None
                )
                
        Initialization function
        
        question is the question to be asked to the participants of the poll
        
        answersobjs is a list of tuples (answer, obj).
        Each answer can have an attached reference to any object.
        
        turns is the number of turns for which the poll will remain active.
        -1 is indefinite

        isActive indicates whether of not the Poll is active
        
        fformat if a function to format the answers and has a single argument,
        the poll object itself and returns a list of formatted strings
        """
        
        fassert = pollassert + "__init__(). "
        assert question.__class__ == str, fassert + "Question not a string"
        for (answer, obj) in answersobjs:
            assert answer.__class__ == str, fassert + "answer not a string"
        assert turns.__class__ == int, fassert + "Turns not an integer"
        assert turns == INDEF or turns >= 1, fassert + "turns must be ==-1 or >=1"
        assert isactive.__class__ == bool, fassert + "isactive not boolean"
        assert fformat.__class__.__name__ == 'function', fassert + "fformat not a function"
            
        ##The question for which the Poll is computing votes
        self.question = question
        
        ##The list of possible answers, each one with a possible object attached
        #and the number of votes received
        self.data = [[answer, obj, 0] for (answer, obj) in answersobjs]
        
        ##The number of turns left before the Poll expires
        self.turns = turns
        
        ##Boolean to indicate if the Poll is active
        self.isactive = isactive
        
        ##Function to format the strings to be displayed
        self.fformat = fformat
    
 
    def computeVote(self, answer, votes = 1):
        """Poll.computeVote(self, answer, votes = 1)
        Computes votes to one of the Polls answers
        the answer can be either a string or the index in self.data
        """
        
        fassert = pollassert + "computeVote(). "
        assert answer.__class__ in [int, str], fassert + "answer not int or str"
        assert votes.__class__ == int, fassert + "votes not integer"
        
        if answer.__class__ == int and 0 <= answer < len(self.data):
            self.data[answer][VOTES] += votes
            return True
        elif ( answer.__class__ == str
               and answer in [ datum[ANSWER] for datum in self.data ]
             ):
            i = [ datum[ANSWER] for datum in self.data ].index(answer)
            self.data[i][VOTES] += votes
            return True
        else:   
            return False
  
    
    def getRank(self):
        """Poll.getRank(self)
        Returns the Poll's results ordered by most voted answers
        """
        
        rank = list(self.data)
        rank.sort( lambda x, y: -1 if x[VOTES] < y[VOTES]
                                   else (0 if x[VOTES] == y[VOTES] else 1),
                   reverse = True
                 )
        return rank
        
    
    def getWinner(self):
        """Poll.getWinner(self)
        Returns the Poll's winning answer
        """
        
        return max(self.data, key = lambda datum: datum[VOTES])
        
   
    def newTurn(self, turnnumber = 1):
        """Poll.newTurn(self, turnnumber = 1)
        Function to compute a new turn
        """
        
        fassert = pollassert + "newTurn(). "
        assert turnnumber.__class__ == int, fassert + "turnnumber not an integer"
        assert turnnumber >= 1, fassert + "invalid turnnumber"
        
        if self.turns != INDEF and self.isactive:
            self.turns -= turnnumber
            if self.turns == 0:
                self.isactive = False
                
  
    def formattedstr(self):
        """Poll.formattedstr(self)
        Returns a list of the Poll's formatted strings.
        The first one being the question and the others the answers, in order
        """
        
        return self.fformat(self)
        
    def introduction(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a first introduction of the object,
        to receivers that are unaware of its existence.
        """
        frmtd = self.fformat(self)
        r = [("class", self.__class__.__name__),
             ("question", frmtd[0])
            ]
        
        for i in range( 1, len(frmtd) ):
            r.append( ( "answer obj votes " + str(i), (frmtd[i],
                                                       self.data[i-1][OBJECT].objid,
                                                       self.data[i-1][VOTES]
                                                      )
                      )
                    )
        
        r += [("turns", self.turns), ("isactive", self.isactive)]
        
        return dict(r)
    
    def catchingUp(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a update on the object's state,
        sent to receivers that are already able to identify the object.
        """
        return self.introduction()    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                 
