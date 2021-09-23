import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template

import XMPP_credentials as creds

# https://spade-mas.readthedocs.io/en/latest/api.html


class SenderAgent(Agent): 
    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            msg = Message(to=creds.receiver[0])         # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "Hello World"                    # Set the message content

            await self.send(msg)
            print("Message sent!")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("SenderAgent started")
        b = self.InformBehav()
        self.add_behaviour(b)

class ReceiverAgent(Agent):
    class RecvBehav(OneShotBehaviour):
        async def run(self):
            print("RecvBehav running")

            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
            else:
                print("Did not received any message after 10 seconds")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
        
        
class KMAgent(Agent):
    # Template matching the request for supplier names
    sup_name_temp = Template(sender=creds.ssa[0],
                             body="supplier names", 
                             metadata={"performative": "request"})
    # Template matching the inform of the supplier ranking
    sup_rank_temp = Template(sender=creds.ssa[0], 
                             metadata={"performative": "inform",
                                       "ontology": "supplier rankings"})
    
    class KMAgentBehav(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.supplier_ranking = None                                 # init
            self.supplier_names = f"{{{creds.sa1[0]}, {creds.sa2[0]}}}"  # init supplier names with their IDs in .json string format
        
        async def run(self):
            msg = await self.receive()  # wait to receive a message
            if KMAgent.sup_name_temp.match(msg):  # If the supplier name request template matches the message
                resp = Message(to=msg.sender,  # Construct message containing supplier names
                               body=str(self.supplier_names))
                
                await self.send(resp)  # Send message
                
            elif KMAgent.sup_rank_temp.matches(msg):  # If the supplier ranking information template matches the message
                self.supplier_ranking = msg.body  # Set the ranking to be the message body
                
                notif = Message(to=creds.ssa[0],  # Construct a message informing that the ranking has been stored
                                body="stored supplier rankings",
                                metadata={"performative": "inform"})
                
                await self.send(notif)  # Send message
        
    async def setup(self):
        b = self.KMAgentBehav()
        # t = Template()
        # t.add_metadata("sender", "sender@server")
        self.add_behaviour(b, template=None)
        
        
class OAAgent(Agent):
    #Template for an Order Allocation Task request from CA
    order_alloc_temp = Template(sender=creds.ca[0], 
                             metadata={"performative": "request"})
    
    #Template for information from KMA
    data_temp = Template(sender=creds.kma[0],
                        metadata={"performative", "inform"})

    #Template for optimization results from OA
    opt_results_temp = Template(sender=creds.oa[0],
                            metadata={"performative", "inform"})

    class OAAgentBehav(CyclicBehaviour):
        def ___init__(self):
            super().__init__()

        async def run(self):
            #Wait to receive a message from the server
            msg = await self.receive()

            #Message from CA to start order allocation task
            if msg.match(OAAgent.order_alloc_temp):
                #Request to KMA for supplier ranking results and product data
                req = Message(sender=creds.oaa[0],
                        to=creds.kma[0],
                        body="supplier ranking results, product data",
                        metadata=("performative", "request"))
                
                await self.send(req)
            
            #Message from KMA with supplier ranking results and product data
            if msg.match(OAAgent.data_temp):
                #Bi-Objective model to allocate orders
                model = 69.420

                req = Message(sender=creds.oaa[0],
                        to=creds.oa[0],
                        body=model,
                        metadata=("performative", "request-inform"))

                await self.send(req)
                        
            #Message from OA with optimization results            
            if msg.match(OAAgent.opt_results_temp):
                inf_CA = Message(sender=creds.oaa[0],
                            to=creds.ca[0],
                            body=msg.body,
                            metadata=("performative", "inform"))

                await self.send(inf_CA)

                inf_KMA = Message(sender=creds.oaa[0],
                            to=creds.kma[0],
                            body=msg.body,
                            metadata=("performative","inform"))

                await self.send(inf_KMA)
                
        async def setup(self):
            b = self.OAAgentBehav()
            t = Template()
            #specifies name of sender
            t.sender = creds.ooa[0]
            self.add_behaviour(b, t)
           
           
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

 
class PRAgent(Agent):
    class PRAgentBehav(CyclicBehaviour):
        def ___init__(self):
                super().__init__()
        
        async def on_start(self):
            msg = Message(to=creds.ca[0], body= "rank suppliers")
            msg.set_metadata("performative", "request")
            await self.send(msg)       
        
        async def run(self):
            msg = await self.receive()
            
            if msg.sender == "masb6-ca@01337.io":
                if msg.body == "stored supplier rankings":
                    msg = Message(to=creds.ca[0], body= "order allocation")
                    msg.set_metadata("performative", "request")
                elif msg.body == "order allocation done":
                    msg = Message(to=creds.ca[0], body= "routing")
                    msg.set_metadata("performative", "request")
                await self.send(msg)
        
    async def setup(self):
        b = self.PRAgentBehav()
        t= Template()
        t.sender = creds.ca[0]
        t.set_metadata("performative", "inform")
        self.add_behaviour(b, t)
        
        
class CAgent(Agent):
    class CAgentBehav(OneShotBehaviour):
        def ___init__(self):
                super().__init__()
        
        async def run(self):
            await msg = self.receive()
            if msg.sender == "masb6-pra@01337.io":
                msg.to=creds.ssa[0]
                await self.send(msg)
            elif msg.send == "masb6-sender@01337.io":
                if msg.body == "stored supplier ranking":
                    msg.to=creds=pra[0]
                    msg.set_metadata("performative", "inform")
                await self.send(msg)
        
    async def setup(self):
        b = self.CAgentBehav()
        t = Template()
        t.sender = creds.pra[0], creds.ssa[0]
        self.add_behaviour(b, template=None)
        
        
class SSAgent(Agent):
    class SSAgentBehav(OneShotBehaviour):
        async def run(self):
            pass
        
    async def setup(self):
        b = self.SSAgentBehav()
        self.add_behaviour(b, template=None)
        
        
class SAgent(Agent):
    class SAgentBehav(OneShotBehaviour):
        async def run(self):
            await msg = self.receive()
            if msg.sender == creds.ssa[0]:
                if msg.body == "give your rankings":
                    msg = Message(to=creds.ssa[0])
                    msg.body = "supplier info"
                    msg.set_metadata("performative", "inform")
                    await self.send(msg)  
    
    async def setup(self):
        b = self.SAgentBehav()
        t= Template()
        t.sender = creds.ssa[0]
        t.set_metadata("performative", "request")
        self.add_behaviour(b, t)
        
        
class VAgent(Agent):
    class VABehav(CyclicBehaviour):
        async def run(self):
            await msg = self.receive()
            if msg.sender == creds.vra[0]:
                if msg.body == "give your rankings":
                    msg = Message(to=creds.vra[0])
                    msg.body = "vehicle info"
                    msg.set_metadata("performative", "inform")
                    await self.send(msg)
    
        
    async def setup(self):
        raise NotImplementedError
    

if __name__ == "__main__":    
    receiveragent = ReceiverAgent(*creds.receiver) # ReceiverAgent("receiver@01337.io", "receiver-pass")
    future = receiveragent.start()
    future.result() # wait for receiver agent to be prepared.
    senderagent = SenderAgent(*creds.sender)
    senderagent.start()

    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            receiveragent.stop()
            break
    print("Agents finished")
    