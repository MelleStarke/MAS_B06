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
sa5 = agents.SAgent(*creds.sa5, info=dict5)
sa6 = agents.SAgent(*creds.sa6, info=dict6)
sa7 = agents.SAgent(*creds.sa7, info=dict7)
sa8 = agents.SAgent(*creds.sa8, info=dict8)
sa9 = agents.SAgent(*creds.sa9, info=dict9)
sa10 = agents.SAgent(*creds.sa10, info=dict10)

participants = [sa10, sa9, sa8, sa7, sa6, sa5, sa4, sa3, sa2, sa1, kma, ssa, ca, pra]

# future = pra.start()
# future.result()

for p in participants:
    future = p.start(auto_register=True)
    future.result()
