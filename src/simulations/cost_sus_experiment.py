# sys.path.append("..src")
import src.agents as agents
import src.agents.util.agent_credentials as creds

from src.agents.util.supplier_info import *


pra = agents.PRAgent(*creds.pra)
ca = agents.CAgent(*creds.ca)
ssa = agents.SSAgent(*creds.ssa)
kma = agents.KMAgent(*creds.kma)

sa1 = agents.SAgent(*creds.sa1, info=dict1)
sa2 = agents.SAgent(*creds.sa2, info=dict2)
sa3 = agents.SAgent(*creds.sa3, info=dict3)
sa4 = agents.SAgent(*creds.sa4, info=dict4)

participants = [sa4, sa3, sa2, sa1, kma, ssa, ca, pra]

# future = pra.start()
# future.result()

for p in participants:
    future = p.start(auto_register=True)
    future.result()
