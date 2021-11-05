from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from .util import agent_credentials as creds

# Template matching the request to execute the supplier selection task
SS_REQ_TEMP = Template(sender=str(creds.pra[0]),
                       body="start supplier selection",
                       metadata={"performative": "request"})

# Template matching the inform of the supplier selection task being completed
SS_INF_TEMP = Template(sender=str(creds.ssa[0]),
                       body="supplier selection done",
                       metadata={"performative": "inform"})

# Template matching the request to execute the order allocation task
OA_REQ_TEMP = Template(sender=str(creds.pra[0]),
                       metadata={"performative": "request",
                                 "ontology": "order allocation start request"})

# Template matching the inform of the order allocation task being completed
OA_INF_TEMP = Template(sender=str(creds.oaa[0]),
                        body="order allocation done",
                        metadata={"performative": "inform"})

# Template matching the request to execute the vehicle routing task
VR_REQ_TEMP = Template(sender=str(creds.pra[0]),
                       body="start vehicle routing selection",
                       metadata={"performative": "request"})
# Template matching the inform of the vehicle routing task being completed
VR_INF_TEMP = Template(sender=str(creds.vra[0]),
                       body="vehicle routing done",
                       metadata={"performative": "inform"})

# Template matching the kill order by the PRA
KILL_ORDER_TEMP = Template(sender=str(creds.pra[0]),
                           body="stop running",
                           metadata={"performative": "propagate"})


class CAgent(Agent):

    class CAgentBehav(CyclicBehaviour):
        """
        Behaviour for the  Agent.
        """
        async def on_start(self):
            print(f"{self.agent.jid} started")

        async def run(self):
            print(f"{self.agent.jid} waiting on a message")
            msg = await self.receive(timeout=30)
            
            # If no message has been received after the timeout, the message is None
            if msg is None:
                print(f"{self.agent.jid} waiting timed out")
                
            else:
                print(f"{self.agent.jid} received a message")
                
                # Pseudo switch statement for the evaluation of the message. Checks message templates for a match.

                if SS_REQ_TEMP.match(msg):  # Template for the supplier selection start request.
                    req = Message(sender=str(self.agent.jid),
                                  to=creds.ssa[0],
                                  body="start supplier selection",
                                  metadata={"performative": "request"})

                    await self.send(req)
                    print(f"{self.agent.jid} sent a message to {req.to}")

                elif SS_INF_TEMP.match(msg):  # Template for the supplier selection completion message.
                    inf = Message(sender=str(self.agent.jid),
                                  to=creds.pra[0],
                                  body="supplier selection done",
                                  metadata={"performative": "inform"})

                    await self.send(inf)
                    print(f"{self.agent.jid} sent a message to {inf.to}")

                elif OA_REQ_TEMP.match(msg):  # Template for the order allocation start request.
                    req = msg
                    req.sender = str(self.agent.jid)
                    req.to = creds.oaa[0]

                    await self.send(req)
                    print(f"{self.agent.jid} sent a message to {req.to}")

                elif OA_INF_TEMP.match(msg):  # Template for the  order allocation completion message.
                    inf = Message(sender=str(self.agent.jid),
                                  to=creds.pra[0],
                                  body="supplier selection done",
                                  metadata={"performative": "inform"})

                    await self.send(inf)
                    print(f"{self.agent.jid} sent a message to {inf.to}")

                elif VR_REQ_TEMP.match(msg):  # Template for the vehicle routing start request.
                    req = Message(sender=str(self.agent.jid),
                                  to=creds.vra[0],
                                  body="start vehicle routing selection",
                                  metadata={"performative": "request"})
                    print("passing along")
                    await self.send(req)
                    print(f"{self.agent.jid} sent a message to {req.to}")
                    pass
                    pass

                elif VR_INF_TEMP.match(msg):  # Template for the vehicle routing completion message.
                    inf = Message(sender=str(self.agent.jid),
                                  to=creds.pra[0],
                                  body="vehicle routing done",
                                  metadata={"performative": "inform"})

                    await self.send(inf)
                    print(f"{self.agent.jid} sent a message to {inf.to}")
                    pass
                
                elif KILL_ORDER_TEMP.match(msg):
                    self.kill()

                else:
                    print(f"{self.agent.jid} received a message that doesn't match a template from {msg.sender}")
                    
        async def on_end(self):
            print(f"{self.agent.jid} is stopping")
            await self.agent.stop()


    async def setup(self):
        b = self.CAgentBehav()
        self.add_behaviour(b)
        b.set_agent(self)
        