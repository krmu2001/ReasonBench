import random
import logging
import asyncio
from typing import TypedDict
from collections import Counter
from omegaconf import OmegaConf
from ..typedefs import Method, Model, Agent, Environment, DecodingParameters, State, Benchmark, MAX_SEED
from .. import MethodFactory, AgentDictFactory
from ..utils import Resampler
logger = logging.getLogger(__name__)


@AgentDictFactory.register
class AgentDictCoT(TypedDict):
    step: Agent # ActAgent
    step_params: DecodingParameters


@MethodFactory.register
class MethodCOT_SC(Method):
    def __init__(self,
                 model: Model,
                 agents: AgentDictCoT,
                 env: Environment,
                 config: OmegaConf,
                 ):
        super().__init__(model, agents, env, config)

        self.step_agent = agents["step"]
        self.step_params = agents["step_params"]

        self.n = config.n
        assert self.n > 1, "CoT-SC needs at least 2 outputs"
