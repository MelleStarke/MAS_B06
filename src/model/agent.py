from mesa import Agent, Model
from typing import *
from enum import Enum

class MsgMode(Enum):
    INFORM = 0
    REQUEST = 1

Message = Tuple[MsgMode, str]


class S3Agent(Agent):
    def __init__(self, unique_id: int, model: Model):
        self.msg_stack: List[Message] = list()
      
    def send(self, recipient: Agent, msg: Tuple[MsgMode, str]):
        raise NotImplementedError
    
    def receive(self, mode: MsgMode, msg: Message):
        raise NotImplementedError


class SupplierAgent(S3Agent):
    def __init__(self, unique_id: int, model: Model):
        raise NotImplementedError


class SupplierSelectionAgent(S3Agent):
    def __init__(self, unique_id: int, model: Model):
        raise NotImplementedError


class KnowledgeAgent(S3Agent):
    def __init__(self, unique_id: int, model: Model):
        raise NotImplementedError

class ProjectReleaseAgent(S3Agent):
    def __init__(self, unique_id: int, model: Model):
        raise NotImplementedError
