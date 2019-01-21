
from Game import *

s = GameSpace(0.0,
              2.0,
              0.0,
              3.0,
              0.0,
              30.0,
              cellsize = 1.0
             )

t = Team(3, 'timao', [])
t2 = Team(2, 'eo', [])

go = GameObject(1,
                (3.0,4.0,5.0),
                s,
                (0.0,0.0,0.0),
                (1.0,1.0,1.0),
                (0.0,0.0,0.0), [],[],[],[]
               )
               
go2 = GameObject(2,
                (8.0, 15.0, 27.0),
                s,
                (0.0,0.0,0.0),
                (1.0,1.0,1.0),
                (0.0,0.0,0.0), [],[],[],[]
               )
               


l = Layer("default", [go])
l = Layer("alt", [go2])

GameObject.initTagDomain( {'one': 1, 'two': 2} )

go.addTags(['one'])
go2.addTags(['two'])

t.addMembers([go])
t2.addMember(go2)

game = Game('teste', 'jogo teste lol', s, GameObject.gameobjects, Team.teams, True, [])


