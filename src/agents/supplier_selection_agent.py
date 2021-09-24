import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template

from . import agent_credentials as creds

# Template matching the request to execute the supplier selection task
SS_REQ_TEMP = Template(sender=str(creds.ca[0]),
                       body="start supplier selection",
                       metadata={"performative": "request"})

SUP_NAME_INF_TEMP = Template(sender=str(creds.kma[0]),
                             metadata={"performative": "inform",
                                       "ontology": "supplier names"})

SUP_INFO_TEMP = Template(metadata={"performative": "inform",
                                   "ontology": "supplier info"})


class SSAgent(Agent):

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.supplier_names = list()
        self.supplier_info = list()

    class SSAgentBehav(CyclicBehaviour):

        async def on_start(self):
            print(f"{self.agent.jid} started")

        async def run(self):
            print(f"{self.agent.jid} waiting on a message")
            msg = await self.receive(timeout=60)  # Wait to receive a message
            print(f"{self.agent.jid} received a message")

            if SS_REQ_TEMP.match(msg):
                # Ask the Knowledge Agent for a list of suppliers
                req = Message(sender=str(self.agent.jid),
                              to=creds.kma[0],
                              body="supplier names",
                              metadata={"performative": "request"})

                await self.send(req)

            elif SUP_NAME_INF_TEMP.match(msg):
                supplier_names = self.extract_supplier_names(msg.body)
                self.agent.supplier_names = supplier_names

                for supplier in supplier_names:
                    req = Message(sender=str(self.agent.jid),
                                  to=supplier,
                                  body="give me your info")

                    await self.send(req)

            elif SUP_INFO_TEMP.match(msg):
                info = self.extract_supplier_info()
                if info[
                    0] in self.agent.supplier_names:  # If the supplier name of the info is in the list of known supplier names
                    self.agent.supplier_info.append(info)

                if len(self.agent.supplier_names) is len(self.agent.supplier_info):
                    # Send the rankings
                    resp_KMA = Message(sender=str(self.agent.jid),
                                       to=creds.kma[0],
                                       body=str(self.agent.supplier_info),
                                       metadata={"performative": "inform",
                                                 "ontology": "supplier rankings"})

                    await self.send(resp_KMA)

                    resp_CA = Message(sender=str(self.agent.jid),
                                      to=creds.ca[0],
                                      body="supplier selection done",
                                      metadata={"performative": "inform"})

                    await self.send(resp_CA)

        def extract_supplier_names(self, msg_body, ):
            """
            Mock-up for now
            """
            return [creds.sa1[0], creds.sa2[0]]

        def extract_supplier_info(self, msg):
            """
            Mock-up for now
            """
            return "<supplier name>", {"sustainability": 3, "cost": 5}

    async def setup(self):
        b = self.SSAgentBehav()
        self.add_behaviour(b)
        b.set_agent(self)
