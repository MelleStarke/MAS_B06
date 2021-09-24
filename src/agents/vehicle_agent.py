import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template

from . import agent_credentials as creds


class VAgent(Agent):

    class VABehav(CyclicBehaviour):

        async def on_start(self):
            print(f"{self.agent.jid} started")

        async def run(self):
            print(f"{self.agent.jid} waiting on a message")
            msg = await self.receive(timeout=60)  # Wait to receive a message
            print(f"{self.agent.jid} received a message")

            if msg.sender == creds.vra[0]:
                if msg.body == "give your rankings":
                    msg = Message(to=creds.vra[0])
                    msg.body = "vehicle info"
                    msg.set_metadata("performative", "inform")
                    await self.send(msg)
    
        
    async def setup(self):
        raise NotImplementedError
    