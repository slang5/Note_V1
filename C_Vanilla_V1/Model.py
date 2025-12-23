
from typing import Union

from numpy import typing, float64

from C_Vanilla_V1.Option import Option_Call, Option_Put, Digital_Call, Digital_Put
from B_Model_V1.base import SimulationConfig

class Vanilla_Model:
    def __init__(self, option: Union[Option_Call, Option_Put, Digital_Call, Digital_Put], paths: typing.NDArray[float64], config: SimulationConfig):
        self.option = option
        self.paths = paths
        self.config = config


    