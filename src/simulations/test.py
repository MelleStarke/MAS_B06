import sys
#sys.path.append("..src")
import src.agents as agents
import src.agents.agent_credentials as creds

pra = agents.PRAgent(*creds.pra)
ca = agents.CAgent(*creds.ca)
ssa = agents.SSAgent(*creds.ssa)
kma = agents.KMAgent(*creds.kma)
sa1 = agents.SAgent(*creds.sa1, info=dict())
sa2 = agents.SAgent(*creds.sa2, info=dict())

participants = [sa2, sa1, kma, ssa, ca, pra]

#future = pra.start()
#future.result()

for p in participants:
    future = p.start(auto_register=True)
    future.result()
