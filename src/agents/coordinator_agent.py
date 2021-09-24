import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template

from . import agent_credentials as creds


# Template matching the request to execute the supplier selection task
SS_REQ_TEMP = Template(sender=str(creds.pra[0]),
                       body="start supplier selection",
                       metadata={"performative": "request"})

# Template matching the inform of the supplier selection task being completed
SS_INF_TEMP = Template(sender=str(creds.ssa[0]),
                       body="supplier selection done",
                       metadata={"performative": "inform"})

# Template matching the request to execute the order allocation task
OA_REQ_TEMP = Template()

# Template matching the inform of the order allocation task being completed
OA_INF_TEMP = Template()

# Template matching the request to execute the vehicle routing task
VR_REQ_TEMP = Template()

# Template matching the inform of the vehicle routing task being completed
VR_INF_TEMP = Template()


class CAgent(Agent):

    class CAgentBehav(CyclicBehaviour):

        async def on_start(self):
            print(f"{self.agent.jid} started")

        async def run(self):
            print(f"{self.agent.jid} waiting on a message")
            msg = await self.receive(timeout=60)
            print(f"{self.agent.jid} received a message")

            if SS_REQ_TEMP.match(msg):
                print(f"ss req")
                req = Message(sender=str(self.agent.jid),
                              to=creds.ssa[0],
                              body="start supplier selection",
                              metadata={"performative": "request"})
                print("passing along")
                await self.send(req)

            elif SS_INF_TEMP.match(msg):
                inf = Message(sender=str(self.agent.jid),
                              to=creds.pra[0],
                              body="supplier selection done",
                              metadata={"performative": "inform"})

                await self.send(inf)

            elif OA_REQ_TEMP.match(msg):
                """
                Request the Order Allocation Agent to start the order allocation process
                """
                pass

            elif OA_INF_TEMP.match(msg):
                """
                Inform the Project Release Agent that the order allocation process is done
                """
                pass

            elif VR_REQ_TEMP.match(msg):
                """
                Request the Vehicle Routing Agent to start the vehicle routing process
                """
                pass

            elif VR_INF_TEMP.match(msg):
                """
                Inform the Project Release Agent that the vehicle routing process is done
                """
                pass
        
    async def setup(self):
        b = self.CAgentBehav()
        self.add_behaviour(b, template=(SS_REQ_TEMP | SS_INF_TEMP))
        b.set_agent(self)

    @staticmethod
    def am_i_here():
        print("I'm here!")
