from dataclasses import dataclass
from abc import ABC
from typing import Optional

import numpy as np

from timegrid import Calendar

@dataclass(frozen=False)
class SimulationConfig(ABC):
    calendar: Calendar
    n_paths: int
    seed: Optional[int] = None
    antithetic: bool = True

    def __post_init__(self):
        if self.n_paths <= 0:
            raise ValueError("n_paths must be a positive integer")
        
        if self.seed is not None and not isinstance(self.seed, int):
            raise ValueError("seed must be an integer or None")
        
@dataclass(frozen=False)
class PathBlock:
    """
    paths shape: (n_sim, n_steps, d)
    """
    
    n_sim: int
    n_steps: int
    d: int
    seed: Optional[int] = None
    array: Optional[np.typing.NDArray[np.float64]] = None
    
    def __post_init__(self):
        if self.seed is not None:
            np.random.seed(self.seed)

        self.array = np.random.normal(loc=0.0, scale=1.0, size=(self.n_sim, self.n_steps, self.d))
        # turn first row to zeros for initial spot price
        self.array[:, 0, :] = 0.0
        return self.array

