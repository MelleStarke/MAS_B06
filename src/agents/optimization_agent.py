from spade.agent import Agent
from spade.behaviour import CyclicBehaviour


class OAgent(Agent):
    """
    Optimization Agent.
    """

    class OABehav(CyclicBehaviour):
        """
        Behaviour for the Optimization Agent.
        """

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
                    
        async def on_end(self):
            print(f"{self.agent.jid} is stopping")
            await self.agent.stop()
        
    async def setup(self):
        b = self.OABehav()
        self.add_behaviour(b)
        b.set_agent(self)
