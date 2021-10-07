from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from .util import agent_credentials as creds

# Template matching the inform of the supplier selection task being completed
SS_INF_TEMP = Template(sender=str(creds.ca[0]),
                       body="supplier selection done",
                       metadata={"performative": "inform"})

# Template matching the inform of the order allocation task being completed
OA_INF_TEMP = Template()

# Template matching the inform of the vehicle routing task being completed
VR_INF_TEMP = Template()


class PRAgent(Agent):
    """
    Project Release Agent
    """

    class PRAgentBehav(OneShotBehaviour):
        """
        Behaviour of the Project Release Agent
        """
        
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
            
            # If no message has been received after the timeout, the message is None
            if msg is None:
                print(f"{self.agent.jid} waiting timed out")
                
            else:
                print(f"{self.agent.jid} received a message")
                
                # Pseudo switch statement for the evaluation of the message. Checks message templates for a match.
                if SS_INF_TEMP.match(msg):  # Template for the supplier selection completion message.
                    inf = Message(sender=str(self.agent.jid),
                                  to=creds.ca[0],
                                  body="start order allocation",
                                  metadata={"performative": "request"})

                    await self.send(inf)
                    print(f"{self.agent.jid} sent a message")
                    await self.agent.stop()

                elif OA_INF_TEMP.match(msg):  # Template for the order allocation completion message.
                    """
                    Request the Coordinator Agent to start the vehicle routing task
                    """
                    pass

                elif VR_INF_TEMP.match(msg):  # Template for the vehicle routing completion message.
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
