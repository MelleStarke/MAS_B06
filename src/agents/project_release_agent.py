import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template

from . import agent_credentials as creds


# Template matching the inform of the supplier selection task being completed
SS_INF_TEMP = Template(sender=str(creds.ca[0]),
                       body="supplier selection done",
                       metadata={"performative": "inform"})

# Template matching the inform of the order allocation task being completed
OA_INF_TEMP = Template()

# Template matching the inform of the vehicle routing task being completed
VR_INF_TEMP = Template()


class PRAgent(Agent):

    class PRAgentBehav(OneShotBehaviour):
        
        async def on_start(self):
            print(f"{self.agent.jid} started")

        async def run(self):
            init = Message(sender=str(self.agent.jid),
                          to=creds.ca[0],
                          body="start supplier selection",
                          metadata={"performative": "request"})

            await self.send(init)
            print(f"initial message sent")

            print(f"{self.agent.jid} waiting on a message")
            msg = await self.receive(timeout=30)  # Wait to receive a message
            
            if msg is None:
                print(f"{self.agent.jid} waiting timed out")
                
            else:
                print(f"{self.agent.jid} received a message")

                if SS_INF_TEMP.match(msg):
                    inf = Message(sender=str(self.agent.jid),
                                  to=creds.ca[0],
                                  body="start order allocation",
                                  metadata={"performative": "request"})

                    print(f"{self.agent.jid} sending a message")
                    await self.send(inf)
                    print(f"{self.agent.jid} sent a message")
                    await self.agent.stop()

                elif OA_INF_TEMP.match(msg):
                    """
                    Request the Coordinator Agent to start the vehicle routing task
                    """
                    pass

                elif VR_INF_TEMP.match(msg):
                    """
                    Inform the Coordinator Agent to stop all agents
                    """
                    pass

                else:
                    print(f"{self.agent.jid} received a message that doesn't match a template from {msg.sender}")

        
    async def setup(self):
        b = self.PRAgentBehav()
        self.add_behaviour(b, template=(SS_INF_TEMP | OA_INF_TEMP | VR_INF_TEMP))
        b.set_agent(self)
