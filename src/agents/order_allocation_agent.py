import numpy as np
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from .util.mathstuffs import order_perms
import json

from .util import agent_credentials as creds

# Template for an Order Allocation Task request from CA
ORDER_ALLOC_TEMP = Template(sender=str(creds.ca[0]),
                            metadata={"performative": "request",
                                      "ontology": "order allocation start request"})

# Template for information from KMA
DATA_TEMP = Template(sender=str(creds.kma[0]),
                     metadata={"performative": "inform",
                               "ontology": "product data and supplier rankings"})

# Template for optimization results from OA
OPT_RESULTS_TEMP = Template(sender=str(creds.oa[0]),
                            metadata={"performative": "inform"})


class OAAgent(Agent):
    """
    Order Allocation Agent.
    """

    class OAAgentBehav(CyclicBehaviour):
        """
        Behaviour for the Order Allocation Agent.
        """

        def __init__(self):
            super().__init__()
            self.demand = None
            self.alphas = None

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
                if ORDER_ALLOC_TEMP.match(msg):  # Template for the order allocation start request.
                    # Extract order details
                    order_details = json.loads(msg.body.replace("'", '"'))
                    self.demand = order_details['demand']
                    self.alphas = order_details['alphas']

                    # Request to KMA for supplier ranking results and product data
                    req = Message(sender=str(self.agent.jid),
                                  to=creds.kma[0],
                                  body="product data and supplier rankings",
                                  metadata={"performative": "request"})

                    await self.send(req)
                    print(f"{self.agent.jid} sent a message to {req.to}")

                elif DATA_TEMP.match(msg):  # Template for receiving the product data and supplier rankings from the KMA
                    supplier_info = json.loads(msg.body.replace("'", '"'))

                    model = self.create_model(supplier_info)

                    print(f"\n\tOAA finished preparing the Bi-objective Model:\n\t{model}\n")

                    req = Message(sender=str(self.agent.jid),
                                  to=creds.oa[0],
                                  body=str(model),
                                  metadata={"performative": "request",
                                            "ontology": "bi-objective model"})

                    await self.send(req)
                    print(f"{self.agent.jid} sent a message to {req.to}")

                elif OPT_RESULTS_TEMP.match(msg):  # Template for the optimization results message.
                    inf_CA = Message(sender=str(self.agent.jid),
                                     to=creds.ca[0],
                                     body=msg.body,
                                     metadata={"performative": "inform",
                                               "ontology": "optimized order allocation results"})

                    await self.send(inf_CA)

                    inf_KMA = Message(sender=str(self.agent.jid),
                                      to=creds.kma[0],
                                      body=msg.body,
                                      metadata={"performative": "inform",
                                                "ontology": "optimized order allocation results"})

                    await self.send(inf_KMA)

                else:
                    print(f"{self.agent.jid} received a message that doesn't match a template from {msg.sender}")


        def create_model(self, supplier_info):
            prices = supplier_info['purchase prices']
            ranking = supplier_info['ranking']
            demand = self.demand
            n_suppliers = len(ranking)

            order_permutations = order_perms(demand, n_suppliers)
            # Remove duplicates
            order_permutations = {tuple([tuple(y) for y in x]) for x in order_permutations}
            order_permutations = [[list(y) for y in x] for x in order_permutations]

            # Total Purchasing Cost of the order
            def TCP(order):
                return np.sum(np.multiply(np.sum(order, axis=0), prices))

            # Total Sustainability Value of the order
            def TSV(order):
                return np.sum(np.multiply(np.sum(order, axis=0), ranking))

            TCP_min = np.min([TCP(order) for order in order_permutations])
            TSV_max = np.max([TSV(order) for order in order_permutations])

            model = {"TCP_min": TCP_min,
                     "TSV_max": TSV_max,
                     "prices": prices,
                     "ranking": ranking,
                     "demand": demand,
                     "alphas": self.alphas}

            return model

            
        async def on_end(self):
            print(f"{self.agent.jid} is stopping")
            await self.agent.stop()


    async def setup(self):
        b = self.OAAgentBehav()
        self.add_behaviour(b)
        b.set_agent(self)
