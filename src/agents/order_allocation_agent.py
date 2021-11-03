from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import json

from .util import agent_credentials as creds

# Template for an Order Allocation Task request from CA
ORDER_ALLOC_TEMP = Template(sender=str(creds.ca[0]),
                            metadata={"performative": "request"})

# Template for information from KMA
DATA_TEMP = Template(sender=str(creds.kma[0]),
                     metadata={"performative": "inform"})

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
                    # Request to KMA for supplier ranking results and product data
                    req = Message(sender=str(self.agent.jid),
                                  to=creds.kma[0],
                                  body="supplier ranking results, product data",
                                  metadata={"performative": "request"})

                    await self.send(req)
                    print(f"{self.agent.jid} sent a message")

                if DATA_TEMP.match(msg):
                    # Bi-Objective model to allocate orders
                    def tcp(purchase_price, holding_cost, ordering_cost, quantity, available_inventory, order_placed):
                        return (purchase_price * quantity) + (holding_cost * available_inventory) + (ordering_cost * order_placed)
                    
                    self.supplier_info = json.loads(msg.body.replace("'", '"'))

                    req = Message(sender=str(self.agent.jid),
                                  to=creds.oa[0],
                                  body=str(model),
                                  metadata={"performative": "request-inform"})

                    await self.send(req)
                    print(f"{self.agent.jid} sent a message")

                if OPT_RESULTS_TEMP:  # Template for the optimization results message.
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
                    
                    
            def optimize(goal: str):
            """
            Optimized eiher the TCP or TSV
            goal: "TCP" or "TSV"
            """
            
            D = None
            
            Ns = None
            Np = None 
            
            X0 = None  # Order matrix, assume m x n. Initialize arbitrarily, say every value is
            N = None  # nr. of parameters, i.e. nr of cells in X
            max_prod_amount = None  # Maximum quantity of products. e.g. if ordering 5 marbles and 7 raisings then max_order_amount is 7
            
            def tcp(X, P):
                X = np.round(X)
                
                if 
            
            def tsv():
                pass
            
            if goal == "TCP":
                fun = tcp
            elif goal == "TSV":
                fun = tsv
            else:
                raise ValueError("goal must be either TCP or TSV)
            
            bounds = opt.Bounds(np.zeroes(N), np.ones(N) * max_prod_amount)
            res = opt.minimize(fun, X0, args = (None))
            best_order = res.x.reshape(None, None)
            return best_order
            
        async def on_end(self):
            print(f"{self.agent.jid} is stopping")
            await self.agent.stop()


    async def setup(self):
        b = self.OAAgentBehav()
        self.add_behaviour(b)
        b.set_agent(self)
