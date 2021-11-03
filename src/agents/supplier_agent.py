from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from .util import agent_credentials as creds

# Template matching the supplier
INFO_REQ_TEMP = Template(sender=str(creds.ssa[0]),
                         body="give me your info",
                         metadata={"performative": "request"})


class SAgent(Agent):
    """
    Suppplier Agent.
    """

    def __init__(self, jid, password, info: dict):
        super().__init__(jid, password)
        self.info = info

    class SAgentBehav(CyclicBehaviour):
        """
        Behaviour for the Supplier Agent.
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
                if INFO_REQ_TEMP.match(msg):  # Template for the supplier info request.
                    resp = Message(sender=str(self.agent.jid),
                                   to=str(msg.sender),
                                   body=str(self.agent.info),
                                   metadata={"performative": "inform",
                                             "ontology": "supplier info"})
                    await self.send(resp)
                    print(f"{self.agent.jid} sent a message")

                else:
                    print(f"{self.agent.jid} received a message that doesn't match a template from {msg.sender}:\n\t{msg}")
                    
        async def on_end(self):
            print(f"{self.agent.jid} is stopping")
            await self.agent.stop()

# https://www.tutorialspoint.com/How-to-convert-a-string-to-dictionary-in-Python
    
    async def setup(self):
        b = self.SAgentBehav()
        self.add_behaviour(b)
        b.set_agent(self)
        
        