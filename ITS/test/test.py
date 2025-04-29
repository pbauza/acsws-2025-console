import time
from TYPES import Position, Target, Proposal
from Acspy.Clients.SimpleClient import PySimpleClient

p1 = Position(0, 30)
p2 = Position(45, 45)
p3 = Position(45, 15)
t1 = Target(1, p1, 1)
t2 = Target(2, p2, 2)
t3 = Target(3, p3, 3)

c = PySimpleClient()
db = c.getComponent("DATABASE")
pid = db.storeProposal([t1, t2, t3])
print(pid)

p = db.getProposals()
print(p)

co = c.getComponent("CONSOLE")
co.setMode(True)

time.sleep(10)
co.setMode(False)

imgs = db.getProposalObservations(pid-1)
print(imgs)
