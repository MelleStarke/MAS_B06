import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template

from . import agent_credentials as creds

# Template matching the request for supplier names
SUP_NAME_REQ_TEMP = Template(sender=str(creds.ssa[0]),
                             body="supplier names",
                             metadata={"performative": "request"})

# Template matching the inform of the supplier ranking
SUP_RANK_INF_TEMP = Template(sender=str(creds.ssa[0]),
                             metadata={"performative": "inform",
                                       "ontology": "supplier rankings"})


class KMAgent(Agent):
    class KMAgentBehav(CyclicBehaviour):

        def __init__(self):
            super().__init__()
            self.supplier_ranking = None  # init
            self.supplier_names = f"{{{creds.sa1[0]}, {creds.sa2[0]}}}"  # init supplier names with their IDs in .json string format

        async def on_start(self):
            print(f"{self.agent.jid} started")

        async def run(self):
            print(f"{self.agent.jid} waiting on a message")
            msg = await self.receive(timeout=60)  # Wait to receive a message
            print(f"{self.agent.jid} received a message")

            if SUP_NAME_REQ_TEMP.match(msg):  # If the supplier name request template matches the message
                resp = Message(sender=str(self.agent.jid),
                               to=msg.sender,  # Construct message containing supplier names
                               body=str(self.supplier_names))

                await self.send(resp)  # Send message

            elif SUP_RANK_INF_TEMP.match(msg):  # If the supplier ranking information template matches the message
                self.supplier_ranking = msg.body  # Set the ranking to be the message body

                notif = Message(sender=str(self.agent.jid),
                                to=creds.ssa[0],  # Construct a message informing that the ranking has been stored
                                body="stored supplier rankings",
                                metadata={"performative": "inform"})

                await self.send(notif)  # Send message

    async def setup(self):
        b = self.KMAgentBehav()
        self.add_behaviour(b)
        b.set_agent(self)
