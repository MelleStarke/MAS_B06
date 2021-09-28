import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template

from . import agent_credentials as creds

# Template for an Order Allocation Task request from CA
ORDER_ALLOC_TEMP = Template(sender=str(creds.ca[0]),
                            metadata={"performative": "request"})

# Template for information from KMA
DATA_TEMP = Template(sender=str(creds.kma[0]),
                     metadata={"performative": "inform"})

# Template for optimization results from OA
OPT_RESULTS_TEMP = Template(sender=str(creds.oa[0]),
                            metadata={"performative": "inform"})


class OAAgent(Agent):
    class OAAgentBehav(CyclicBehaviour):

        async def on_start(self):
            print(f"{self.agent.jid} started")

        async def run(self):
            print(f"{self.agent.jid} waiting on a message")
            msg = await self.receive(timeout=30)  # Wait to receive a message
            
            if msg is None:
                print(f"{self.agent.jid} waiting timed out")
                
            else:
                print(f"{self.agent.jid} received a message")

                # Message from CA to start order allocation task
                if ORDER_ALLOC_TEMP.match(msg):
                    # Request to KMA for supplier ranking results and product data
                    req = Message(sender=str(self.agent.jid),
                                  to=creds.kma[0],
                                  body="supplier ranking results, product data",
                                  metadata={"performative": "request"})

                    print(f"{self.agent.jid} sending a message")
                    await self.send(req)
                    print(f"{self.agent.jid} sent a message")

                # Message from KMA with supplier ranking results and product data
                if DATA_TEMP.match(msg):
                    # Bi-Objective model to allocate orders
                    model = None

                    req = Message(sender=str(self.agent.jid),
                                  to=creds.oa[0],
                                  body=str(model),
                                  metadata={"performative": "request-inform"})

                    print(f"{self.agent.jid} sending a message")
                    await self.send(req)
                    print(f"{self.agent.jid} sent a message")

                # Message from OA with optimization results
                if OPT_RESULTS_TEMP:
                    inf_CA = Message(sender=str(self.agent.jid),
                                     to=creds.ca[0],
                                     body=msg.body,
                                     metadata={"performative": "inform",
                                               "ontology": "optimized order allocation results"})

                    await self.send(inf_CA)

                    inf_KMA = Message(sender=str(self.agent.jid),
                                      to=creds.kma[0],
                                      body=msg.body,
                                      metadata={"performative": "inform",
                                                "ontology": "optimized order allocation results"})

                    await self.send(inf_KMA)

                else:
                    print(f"{self.agent.jid} received a message that doesn't match a template from {msg.sender}")


    async def setup(self):
        b = self.OAAgentBehav()
        self.add_behaviour(b)
        b.set_agent(self)
