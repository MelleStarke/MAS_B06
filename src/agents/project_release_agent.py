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

    def __init__(self, jid, password, demand, n_suppliers, alphas):
        super().__init__(jid, password)
        self.demand = demand
        self.n_suppliers = n_suppliers
        self.alphas = alphas

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
                    # Order to be optimized
                    order = {"demand": self.agent.demand,
                             "alphas": self.agent.alphas}

                    inf = Message(sender=str(self.agent.jid),
                                  to=creds.ca[0],
                                  body=str(order),
                                  metadata={"performative": "request",
                                            "ontology": "order allocation start request"})

                    await self.send(inf)
                    print(f"{self.agent.jid} sent a message to {inf.to}")

                elif OA_INF_TEMP.match(msg):  # Template for the order allocation completion message.
                    """
                    Request the Coordinator Agent to start the vehicle routing task.
                    For now, it's just an empty block.
                    """
                    # order = Message(sender=str(self.agent.jid),
                    #                 to=creds.ca[0],
                    #                 body="stop running",
                    #                 metadata={"performative": "propagate"})
                    #
                    # await self.send(order)
                    # print(f"{self.agent.jid} sent the kill command")
                    # self.kill()
                    pass
                    

                elif VR_INF_TEMP.match(msg):  # Template for the vehicle routing completion message.
                    """
                    Inform the Coordinator Agent to stop all agents
                    """
                    pass

                else:
                    print(f"{self.agent.jid} received a message that doesn't match a template from {msg.sender}")
                    
        async def on_end(self):
            print(f"{self.agent.jid} is stopping")
            await self.agent.stop()

        
    async def setup(self):
        b = self.PRAgentBehav()
        self.add_behaviour(b)
        b.set_agent(self)
