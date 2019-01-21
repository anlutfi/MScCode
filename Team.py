## @package Team
#File with the Team class definition

teamassert = "Team."
class Team:
    """Represents a Team of GameObjects"""
    
    ##Static list with all the teams
    teams = []
    
    def updateScore(self):
        """Team.updateScore(self)
        Function that calculates the team's score
        """
        self.score = self.fscore(self.members)
        
    def getScore(self):
        """Team.getScore(self)
        The Team's current score
        """
        return self.score
    
    def __init__(self,
                 teamid,
                 name,
                 initialmembers,
                 fscore = lambda members: sum( [member.score for member in members] ),
                ):
        """Team.__init__(self,
                      teamid,
                      name,
                      initialmembers = [],
                      fscore = lambda t: sum( [p.score for p in t.members] ),
                      initialscore = 0
                     )
        Initialization function for a Team object
        
        teamid is an identification number for the team
        name is the team's name
        initialmembers is a initial list of team members (Character objects)
        
        fscore is a function to calculate the teams score. it MUST receive
        a Team object as its only parameter and return the teams score.
        It MUST NOT update the teams score internally.
        """
        
        fassert = teamassert + "__init__(). "
        assert teamid.__class__ == int, fassert + "teamid not int"
        assert teamid not in [t.teamid for t in Team.teams], fassert + "non-unique teamid"
        assert name.__class__ == str, fassert + "team id not str"
        for member in initialmembers:
            assert member.getSuperClassName() == "GameObject", fassert + "member not GameObject"
        assert fscore.__class__.__name__ == 'function', fassert + "fscore not a function"
        
        ##The identification number of a Team
        self.teamid = teamid
        
        ##The Team's name
        self.name = name
        
        ##A list of GameObjects that are members of the Team
        self.members = initialmembers
        for member in self.members:
            member.team = self
        
        ##The Team's current score
        self.score = 0
        
        ##A function to calculate the Team's current score. It MUST NOT set the
        #value of self.score internally, but just return a value
        #self.members must be its only argument
        self.fscore = fscore
                
        self.updateScore()
        
        Team.teams.append(self)
        
    
    def addMember(self, member):
        """Team.addMember(self, member)
        Function to add a team member (Character object) to a Team object
        returns True if the member is inserted and False otherwise.
        Raises an assertionerror if member is not an instance of GameObject
        """
        
        fassert =  teamassert + "addMember(). "
        assert member.getSuperClassName() == 'GameObject', fassert + "member not GameObject"
               
        if member not in self.members:
            self.members.append(member)
            member.team = self
            self.updateScore()
            return True
        return False
        
    
    def addMembers(self, members):
        """Team.addMembers(self, members)
        Adds a list of members (Character object) to a Team object
        If the list contains objects already in the list,
        those objects will not be added
        """
        
        fassert = teamassert + "addMembers(). "
        for member in members:
            assert member.getSuperClassName() == 'GameObject', fassert + "member not a GameObject"
        
        for member in members:
            if member not in self.members:
                self.members.append(member)
                member.team = self
                
        self.updateScore()
        
   
    def removeMember(self, member):
        """Team.removeMember(self, member)
        Removes a member from a Team object.
        Returns True for success and False for failure
        """
        
        try:
            self.members.remove(member)
            member.team = None
            self.updateScore()
            return True
        except ValueError:
            return False
        
    
    def removeMembers(self, members):
        """Team.removeMembers(self, members)
        Removes a list of members (Character object) from a Team object.
        If the list contains objects not in the list they are ignored
        """
        
        for member in members:
            if member in self.members:
                self.members.remove(member)
                member.team = None
        
        self.updateScore()
            
    
    def memberIn(self, member):
        """Team.memberIn(self, member)
        Returns True if member is in the Team and False otherwise.
        Raises an assertionError if member is not a GameObject
        """
        
        fassert = teamassert + "memberIn(). "
        assert member.getSuperClassName() == 'GameObject', fassert + "member not a GameObject"
        
        if member in self.members:
            return True
        return False
        
    def introduction(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a first introduction of the object,
        to receivers that are unaware of its existence.
        """
        return {"class": self.__class__.__name__,
                "teamid": self.teamid,
                "name": self.name,
                "members": [member.objid for member in self.members],
                "score": self.score
               }
    
    def catchingUp(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a update on the object's state,
        sent to receivers that are already able to identify the object.
        """
        return {"class": self.__class__.__name__,
                "teamid": self.teamid,
                "members": [member.objid for member in self.members],
                "score": self.score
               }
               
    @staticmethod
    def getTeamById(teamid):
        """Team.getTeamById(teamid)
        Returns the team in Team.teams whose teamid matches the argument
        or None for no match.
        """
        for l in Team.teams:
            if l.teamid == teamid:
                return l
        return None
        
    @staticmethod
    def getTeamByName(name):
        """Team.getTeamByName(name)
        Returns the team in Team.teams whose name matches the argument
        or None for no match.
        """
        for l in Team.teams:
            if l.name == name:
                return l
        return None
             
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
