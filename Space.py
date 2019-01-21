##@package Space
# File containing Cell, Grid and GameSpace class definitions


from GameObject import GameObject

X = 0
Y = 1
Z = 2

D3 = 3
D2 = 2

cellassert = "Cell."
class Cell:
    """a Grid object's cell"""
    
    def __init__(self, xb, xe, yb, ye):
        """Cell.__init__(self, xb, xe, yb, ye)
        Initialization function for a Cell Object
        
        xb is xbegin
        xe in xend
        
        same for yb and ye
        """
        
        fassert = cellassert + "__init__(). "
        assert xb.__class__ == float, fassert + "xb not float"
        assert xe.__class__ == float, fassert + "xb not float"
        assert yb.__class__ == float, fassert + "xb not float"
        assert ye.__class__ == float, fassert + "xb not float"
                
        ##x begin, lowest x coordinate that is in the cell
        self.xb = xb
        
        ##x end, highest x coordinate that is in the cell
        self.xe = xe
        
        
        ##y begin, lowest y coordinate that is in the cell
        self.yb = yb
        
        ##y end, highest y coordinate that is in the cell
        self.ye = ye
        
        ##List of GameObjects (GameObject) currently in the Cell
        self.gameobjects = []
    
  
    def center(self):
        """Cell.center(self)
        Returns the (X, Y) coordinate of the Cell's center point
        """
        return ( (self.xb + self.xe) / 2, (self.yb + self.ye) / 2, 0 )
    
    def addObject(self, obj):
        """Cell.addObject(obj)
        adds a GameObject obj to the cell's gameobjects[].
        Returns True for success and False for failure
        """
        
        fassert = cellassert + "addObject()."
        assert obj.getSuperClassName() == 'GameObject', fassert + "obj not instance of GameObject"
        
        if obj not in self.gameobjects:
            self.gameobjects.append(obj)
            return True
        return False
        
   
    def removeObject(self, obj):
        """Cell.removeObject(obj)
        removes a GameObject obj from the cell's gameobjects[].
        """
        
        try:        
            self.gameobjects.remove(obj)
            return True
        except ValueError:
            return False
        
  
    def getObjects(self):
        """Cell.getObjects()
        returns a list of game objects located in the Cell
        """
        return self.gameobjects
        
    def introduction(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a first introduction of the object,
        to receivers that are unaware of its existence.
        """
        return {"class": self.__class__.__name__,
                "xb": self.xb,
                "xe": self.xe,
                "yb": self.yb,
                "ye": self.ye,
                "gameobjects": [obj.objid for obj in self.gameobjects]
               }
                
    def catchingUp(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a update on the object's state,
        sent to receivers that are already able to identify the object.
        """
        return self.introduction()
  
    
gridassert = "Grid."
class Grid:
    """Class that divides a GameSpace object's floor plane in a grid"""
    
    def __init__(self, xmin, xmax, ymin, ymax, cellsize):
        """Grid.___init(xmin, xmax, ymin, ymax, cellsize)
        Initialization Function for a Grid object
        
        xmin is the lowest x coordinate
        xmax is the highest x coordinate
        
        ymin is the lowest y coordinate
        ymax is the highest y coordinate
        
        cellsize is the size of each cell
        """
        
        fassert = gridassert + "__init__(). "
        
        assert xmin.__class__ == float, fassert + "xmin not float"
        assert xmax.__class__ == float, fassert + "xmax not float"
        assert ymin.__class__ == float, fassert + "ymin not float"
        assert ymax.__class__ == float, fassert + "ymax not float"
        assert cellsize.__class__ == float, fassert + "cellsize not float"
        assert xmax - xmin >= cellsize, fassert + "a single cell does not fit in the grid (xmax - xmin >= cellsize)"
        assert ymax - ymin >= cellsize, fassert + "a single cell does not fit in the grid (ymax - ymin >= cellsize)"
        
        ##The size of a Cell
        self.cellsize = cellsize
        
        ##The lowest x coordinate in the Grid
        self.xmin = xmin
        
        ##The highest x coordinate in the Grid
        self.xmax = xmax
        
        ##The lowest y coordinate in the Grid      
        self.ymin = ymin
        
        ##The highest y coordinate in the Grid
        self.ymax = ymax
        
        ##Grid's Cell matrix
        self.g = [ [Cell(i * cellsize, i * cellsize + cellsize,
                         j * cellsize, j * cellsize + cellsize
                        )
                    for j in range(  int( ( self.ymax - self.ymin ) / cellsize )  )
                   ] for i in range(  int( ( self.xmax - self.xmin ) / cellsize )  )
                 ]
                 
 
    def getGridPosition(self, pos):
        """Grid.getGridPosition(pos)
        cell coordinates of a given 3d or 2d position pos
        """
        
        #assert pos.__class__ == numpy.ndarray, fassert + "pos not numpy.ndarray"
        
        return ( int(pos[X] / self.cellsize), int(pos[Y] / self.cellsize) )
        
   
    def getCellObjects(self, x, y):
        """Grid.getCellObjects(x, y)
        return the list of GameObjects in the x,y cell
        """
        
        try:
            return self.g[x][y].getObjects()
        except IndexError:
            return None  
            
    
    def introduction(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a first introduction of the object,
        to receivers that are unaware of its existence.
        """
        return {"class": self.__class__.__name__,
                "xmin": self.xmin,
                "xmax": self.xmax,
                "ymin": self.ymin,
                "ymax": self.ymax,
                "cellsize": self.cellsize,
                "g": dict( [((i, j), self.g[i][j].introduction())
                            for i in range(  int( (self.xmax - self.xmin)
                                                  / self.cellsize
                                                ) 
                                          )
                            for j in range(  int( (self.ymax - self.ymin)
                                                  / self.cellsize
                                                ) 
                                          )
                           ]
                         )
               }
                
    def catchingUp(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a update on the object's state,
        sent to receivers that are already able to identify the object.
        """                       
        return {"class": self.__class__.__name__,
                "xmin": self.xmin,
                "xmax": self.xmax,
                "ymin": self.ymin,
                "ymax": self.ymax,
                "cellsize": self.cellsize,
                "g": dict( [((i, j), self.g[i][j].catchingUp())
                            for i in range(  int( (self.xmax - self.xmin)
                                                  / self.cellsize
                                                )
                                          )
                            for j in range(  int( (self.ymax - self.ymin)
                                                  / self.cellsize
                                                )
                                          )
                           ]
                         )
               }
    
        
gamespaceassert = "GameSpace."
class GameSpace:
    """Class that defines the game's 3d coordinate system"""
    
    def __init__(self,
                 xmin,
                 xmax,
                 ymin,
                 ymax,
                 zmin,
                 zmax,
                 origin = (0, 0, 0),
                 cellsize = 0.0
                ):
        """GameSpace.__init__(xmin,
                 xmax,
                 ymin,
                 ymax,
                 zmin,
                 zmax,
                 origin,
                 cellsize = 0.0
                )
        Initialization Function for a GameSpace Object
        
        xmin is the lowest x coordinate
        xmax is the highest x coordinate
        
        ymin is the lowest y coordinate
        ymax is the highest y coordinate
        
        zmin is the lowest z coordinate
        zmax is the highest z coordinate
        
        origin is a tuple (x,y,z) that sets the systems origin
        
        cellsize is the size of a cell in a grid to be superimposed over the floor.
        a zero size indicates there will be no grid
        """
        
        fassert = gamespaceassert + "__init__(). "
        assert xmin.__class__ == float, fassert + "xmin not float"
        assert xmax.__class__ == float, fassert + "xmax not float"
        assert ymin.__class__ == float, fassert + "ymin not float"
        assert ymax.__class__ == float, fassert + "ymax not float"
        assert zmin.__class__ == float, fassert + "zmin not float"
        assert zmax.__class__ == float, fassert + "zmax not float"
        #assert origin.__class__ == numpy.ndarray, fassert + "origin not numpy.ndarray"
        assert cellsize.__class__ == float, fassert + "cellsize not float"
       
        assert (xmin <= xmax), fassert + "xmin < xmax"
        assert (ymin <= ymax), fassert + "ymin < ymax"
        assert (zmin <= zmax), fassert + "zmin < zmax"
        
        assert (len(origin) == D3
                and xmin <= origin[X] <= xmax
                and ymin <= origin[Y] <= ymax
                and zmin <= origin[Z] <= zmax
               ), fassert + "invalid origin"
        
        assert cellsize >= 0, fassert + "invalid cellsize"
        
        ##Lowest x coordinate in GameSpace
        self.xmin = xmin
        
        ##Highest x coordinate in GameSpace
        self.xmax = xmax
        
        ##Lowest y coordinate in GameSpace
        self.ymin = ymin
        
        ##Highest y coordinate in GameSpace
        self.ymax = ymax
        
        ##Lowest z coordinate in GameSpace
        self.zmin = zmin
        
        ##Highest z coordinate in GameSpace
        self.zmax = zmax
        
        ##3D origin of GameSpace
        self.origin = origin
        
        ##An object of Class Grid.
        #If not None, it divides the GameSpace's ground plane in Cell's
        self.grid = None
        
        if cellsize != 0:
            self.grid = Grid(xmin, xmax, ymin, ymax, cellsize)
        
        
    def introduction(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a first introduction of the object,
        to receivers that are unaware of its existence.
        """
        return {"class": self.__class__.__name__,
                "xmin": self.xmin,
                "xmax": self.xmax,
                "ymin": self.ymin,
                "ymax": self.ymax,
                "zmin": self.zmin,
                "zmax": self.zmax,
                "origin": self.origin,
                "grid": None if self.grid == None else self.grid.introduction()
               }
                
    def catchingUp(self):
        """Generates a JSON friendly dictionary with
        all the object's attributes and values.
        This function is intended as a update on the object's state,
        sent to receivers that are already able to identify the object.
        """
        return {"class": self.__class__.__name__,
                "xmin": self.xmin,
                "xmax": self.xmax,
                "ymin": self.ymin,
                "ymax": self.ymax,
                "zmin": self.zmin,
                "zmax": self.zmax,
                "origin": self.origin,
                "grid": None if self.grid == None else self.grid.catchingUp()
               }
        
    
            
               
        
        
