from skeletons.environments import VacuumWorld
from skeletons.agents import Vacuum


vw = VacuumWorld(col=4, row=4)
vac_agent = Vacuum(name='vac1', environment=vw)

print(vw.space.grid)

