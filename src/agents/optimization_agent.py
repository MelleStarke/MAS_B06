from matplotlib import pyplot as plt
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import json
import numpy as np

from .util import agent_credentials as creds
from .util.mathstuffs import order_perms


# Template for the Bi-Objective Model Optimization request from OAA
OAA_OPT_REQ_TEMP = Template(sender=str(creds.oaa[0]),
                            metadata={"performative": "request",
                                      "ontology": "bi-objective model"})


class OAgent(Agent):
    """
    Optimization Agent.
    """

    class OABehav(CyclicBehaviour):
        """
        Behaviour for the Optimization Agent.
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
                if OAA_OPT_REQ_TEMP.match(msg):  # Template for the optimization request from OAA
                    model = json.loads(msg.body.replace("'", '"'))

                    self.optimize_and_plot_OAA_model(model)

        def optimize_and_plot_OAA_model(self, model):
            TCP_min = model["TCP_min"]
            TSV_max = model["TSV_max"]
            prices = model["prices"]
            ranking = model["ranking"]
            demand = model["demand"]
            alphas = model["alphas"]
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

            # Relative distance from the TCP of the order to TCP_min
            def TCP_distance(order):
                return (TCP(order) - TCP_min) / TCP_min

            # Relative distance from the TSV of the order to TSV_max
            def TSV_distance(order):
                return (TSV_max - TSV(order)) / TSV_max

            # Optimization target function
            def target_fun(order, alpha):
                return alpha * TCP_distance(order) + (1 - alpha) * TSV_distance(order)

            # Index of the best order according to the target function under a certain alpha
            def opt_target_fun_order_idx(alpha):
                return np.argmin([target_fun(order, alpha) for order in order_permutations])

            opt_target_fun_idxs = [opt_target_fun_order_idx(alpha) for alpha in np.arange(*alphas)]

            print(f"\n\tOA found the best order allocations for all alphas. Proceeding to plot.\n")

            alphas = np.arange(*alphas)
            optimal_orders = [order_permutations[i] for i in opt_target_fun_idxs]

            f = plt.figure()
            plt.plot(alphas, [target_fun(o, a) for (o, a) in zip(optimal_orders, alphas)], linestyle="--",
                     label="target function")
            plt.plot(alphas, [TCP_distance(o) for o in optimal_orders], label=r"$d_{TCP}$")
            plt.plot(alphas, [TSV_distance(o) for o in optimal_orders], label=r"$d_{TSV}$")
            plt.title(r"Effect of $\alpha$ on TCP and TSV distances" + "\nand target function score")
            plt.xlabel(r"$\alpha$")
            plt.ylabel("Distance to best order allocation")
            plt.legend()
            plt.show()
            #f.savefig("results.pdf", format="pdf")

        async def on_end(self):
            print(f"{self.agent.jid} is stopping")
            await self.agent.stop()
        
    async def setup(self):
        b = self.OABehav()
        self.add_behaviour(b)
        b.set_agent(self)
