from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from .util import agent_credentials as creds

# Template matching the request for supplier names
SUP_NAME_REQ_TEMP = Template(sender=str(creds.ssa[0]),
                             body="supplier names",
                             metadata={"performative": "request"})

# Template matching the inform of the supplier ranking
SUP_RANK_INF_TEMP = Template(sender=str(creds.ssa[0]),
                             metadata={"performative": "inform",
                                       "ontology": "supplier rankings"})


class KMAgent(Agent):
    """
    Knowledge Agent.
    """

    class KMAgentBehav(CyclicBehaviour):
        """
        Behaviour for the Knowledge Agent.
        """

        def __init__(self):
            super().__init__()
            self.supplier_ranking = None  # init
            self.supplier_names = f"{{{creds.sa1[0]}, {creds.sa2[0]}, {creds.sa3[0]}, {creds.sa4[0]}, {creds.sa5[0]}," \
                                  f"{creds.sa6[0]}, {creds.sa7[0]}, {creds.sa8[0]}, {creds.sa9[0]}, {creds.sa10[0]}}}"  # init supplier names with their IDs in .json string format

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
                if SUP_NAME_REQ_TEMP.match(msg):  # Template for the supplier name list request.
                    resp = Message(sender=str(self.agent.jid),
                                   to=str(msg.sender),  # Construct message containing supplier names.
                                   body=str(self.supplier_names),
                                   metadata={"performative": "inform",
                                             "ontology": "supplier names"})

                    await self.send(resp)
                    print(f"{self.agent.jid} sent a message")  # Send message

                elif SUP_RANK_INF_TEMP.match(msg):  # Template for the supplier rank information message.
                    self.supplier_ranking = msg.body  # Set the ranking to be the message body.
                    print(f"Received rankings: {msg.body}")
                    notif = Message(sender=str(self.agent.jid),
                                    to=creds.ssa[0],  # Construct a message informing that the ranking has been stored.
                                    body="stored supplier rankings",
                                    metadata={"performative": "inform"})

                    await self.send(notif)  # Send message

                else:
                    print(f"{self.agent.jid} received a message that doesn't match a template from {msg.sender}")

    async def setup(self):
        b = self.KMAgentBehav()
        self.add_behaviour(b)
        b.set_agent(self)
