import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import pandas as pd
import json
import scipy.optimize as opt
# import numpy as np
from re import subn
from math import rounded

from .util import agent_credentials as creds
from .util import mathstuffs

# Template matching the request to execute the supplier selection task.
SS_REQ_TEMP = Template(sender=str(creds.ca[0]),
                       body="start supplier selection",
                       metadata={"performative": "request"})

# Template matching the inform of the supplier names.
SUP_NAME_INF_TEMP = Template(sender=str(creds.kma[0]),
                             metadata={"performative": "inform",
                                       "ontology": "supplier names"})

# Template matching the supplier info inform.
SUP_INFO_TEMP = Template(metadata={"performative": "inform",
                                   "ontology": "supplier info"})


class SSAgent(Agent):
    """
    Supplier Selection Agent.
    """

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.supplier_names = list()
        self.supplier_info = list()

    class SSAgentBehav(CyclicBehaviour):
        """
        Behaviour for the Supplier Selection Agent.
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
                if SS_REQ_TEMP.match(msg):  # Template for the supplier selection start request
                    # Ask the Knowledge Agent for a list of suppliers
                    req = Message(sender=str(self.agent.jid),
                                  to=creds.kma[0],
                                  body="supplier names",
                                  metadata={"performative": "request"})

                    await self.send(req)
                    print(f"{self.agent.jid} sent a message")

                elif SUP_NAME_INF_TEMP.match(msg):  # Template for the supplier name message from KMA
                    supplier_names = self.extract_supplier_names(msg.body)
                    self.agent.supplier_names = supplier_names
                    self.agent.supplier_info = [None for x in range(len(supplier_names))]  # Initialize as list of None

                    for supplier in supplier_names:
                        # Ask suppliers for their info
                        req = Message(sender=str(self.agent.jid),
                                      to=supplier,
                                      body="give me your info",
                                      metadata={"performative": "request"})

                        await self.send(req)
                        print(f"{self.agent.jid} sent a message")

                elif SUP_INFO_TEMP.match(msg):  # Template for the supplier info messages from the suppliers themselves
                    info = self.extract_supplier_info(msg.body)
                    if info['Supplier Name'] in self.agent.supplier_names:  # If the sender of the info is in the list of known supplier names
                        supplier_index = self.agent.supplier_names.index(info['Supplier Name'])
                        self.agent.supplier_info[supplier_index] = info

                    # True if self.agent.supplier_info doesn't contain 'None' values. False otherwise.
                    if all(map(lambda x: x is not None, self.agent.supplier_info)):
                        supplier_ranking = self.perform_TOPSIS()

                        resp_KMA = Message(sender=str(self.agent.jid),
                                           to=creds.kma[0],
                                           body=str(supplier_ranking),
                                           metadata={"performative": "inform",
                                                     "ontology": "supplier rankings"})

                        await self.send(resp_KMA)

                        resp_CA = Message(sender=str(self.agent.jid),
                                          to=creds.ca[0],
                                          body="supplier selection done",
                                          metadata={"performative": "inform"})

                        await self.send(resp_CA)

                else:

                    print(f"{self.agent.jid} received a message that doesn't match a template from {msg.sender}")

        def extract_supplier_names(self, msg_body):
            """
            Extracts the supplier names from the message into a list.
            """
            formatted_body, _ = subn(r"\{|\s|\}", '', msg_body)
            return formatted_body.split(",")

        def extract_supplier_info(self, msg_body):
            """
            Extracts the supplier info from the message and turns it back into a dictionary.
            """
            return json.loads(msg_body.replace("'", '"'))

        def perform_TOPSIS(self):
            """
            Ranks the suppliers using TOPSIS.
            Adapted from https://www.geeksforgeeks.org/topsis-method-for-multiple-criteria-decision-making-mcdm/.
            """
            # now we convert all the dictonaries we have, to a dataframe  which makes it easier to work on topsis
            df = pd.DataFrame(self.agent.supplier_info)
            rankings = mathstuffs.perform_TOPSIS(df, self.agent.supplier_names)
            return rankings
        
        
        
                    
        async def on_end(self):
            print(f"{self.agent.jid} is stopping")
            await self.agent.stop()

    async def setup(self):
        b = self.SSAgentBehav()
        self.add_behaviour(b)
        b.set_agent(self)
