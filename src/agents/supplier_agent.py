import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template

from . import agent_credentials as creds


INFO_REQ_TEMP = Template(sender=str(creds.ssa[0]),
                         body="give me your info",
                         metadata={"performative": "request"})


class SAgent(Agent):

    def __init__(self, jid, password, info: dict):
        super().__init__(jid, password)
        self.info = info

    class SAgentBehav(CyclicBehaviour):

        async def on_start(self):
            print(f"{self.agent.jid} started")

        async def run(self):
            print(f"{self.agent.jid} waiting on a message")
            msg = await self.receive(timeout=30)  # Wait to receive a message

            if msg is None:
                print(f"{self.agent.jid} waiting timed out")

            else:
                print(f"{self.agent.jid} received a message")
                if INFO_REQ_TEMP.match(msg):
                    resp = Message(sender=str(self.agent.jid),
                                   to=str(msg.sender),
                                   body=str(self.agent.info),
                                   metadata={"performative": "inform",
                                             "ontology": "supplier info"})
                    print(f"{self.agent.jid} sending a message")
                    await self.send(resp)
                    print(f"{self.agent.jid} sent a message")

                else:
                    print(f"{self.agent.jid} received a message that doesn't match a template from {msg.sender}")

    
    async def setup(self):
        b = self.SAgentBehav()
        self.add_behaviour(b)
        b.set_agent(self)
        
        