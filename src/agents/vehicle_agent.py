from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from .util import agent_credentials as creds


class VAgent(Agent):
    """
    Vehicle Agent.
    """

    class VABehav(CyclicBehaviour):
        """
        Behaviour for the Vehicle Agent.
        """

        async def on_start(self):
            print(f"{self.agent.jid} started")

        async def run(self):
            print(f"{self.agent.jid} waiting on a message")
            msg = await self.receive(timeout=30)  # Wait to receive a message
            
            # If no message has been received after the timeout, the message is None
            if msg is None:
                print(f"{self.agent.jid} waiting timed out")
                
            else:
                print(f"{self.agent.jid} received a message")
                
                # Pseudo switch statement for the evaluation of the message. Checks message templates for a match.
                if msg.sender == creds.vra[0]:
                    if msg.body == "give your rankings":
                        msg = Message(to=creds.vra[0])
                        msg.body = "vehicle info"
                        msg.set_metadata("performative", "inform")
                        await self.send(msg)
                    print(f"{self.agent.jid} sent a message")

                else:
                    print(f"{self.agent.jid} received a message that doesn't match a template from {msg.sender}")

    
        
    async def setup(self):
        raise NotImplementedError
    