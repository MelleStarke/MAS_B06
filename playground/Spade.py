import time
import asyncio
from spade import quit_spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
from spade.container import Container

import XMPP_credentials as creds

class DummyAgent(Agent):
    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))

dummy = DummyAgent(*creds.sender)

#loop = asyncio.ProactorEventLoop()
#asyncio.set_event_loop(loop)

#dummy.set_loop(loop)

future = dummy.start()
future.result()

dummy.stop()
quit_spade()
