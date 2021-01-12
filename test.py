from skeletons.environments import VacuumWorld
from skeletons.agents import Vacuum

vac_agent = Vacuum()
vw = VacuumWorld(agents=[vac_agent], col=2, row=2)
vac_agent.environment = vw

print('done')
