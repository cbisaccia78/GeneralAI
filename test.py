from skeletons.environments import VacuumWorld
from skeletons.agents import Vacuum


vw = VacuumWorld(col=2, row=2)
vac_agent = Vacuum(name='vac1', environment=vw)

print('done')
