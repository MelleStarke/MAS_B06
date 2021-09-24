import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template

from . import agent_credentials as creds


class OAgent(Agent):
    class OABehav(CyclicBehaviour):
        async def run(self):
            """
            receive message from OOA or VRA
            
            if from OOA:
                extract supplier data from OOA's message
                extract product data from OOA's message
                extract the bi-objective model from OOA's message
                maximize the order allocation target function using Scipy's optimization function
                respond with the optimized result
                
            if from VRA:
                extract supplier data from VRA's message
                extract product data from VRA's message
                extract vehicle agent data from VRA's message
                extract the bi-objective model from VRA's message
                maximize the vehicle routing target function using Scipy's optimization function
                respond with the optimized result
            """
            raise NotImplementedError
        
    async def setup(self):
        b = self.OABehav()
        self.add_behaviour(b)
        b.set_agent(self)
