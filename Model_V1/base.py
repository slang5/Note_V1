from dataclasses import dataclass
from abc import ABC
from typing import Optional, Literal

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
    antithetic: bool = False
    array: Optional[np.typing.NDArray[np.float64]] = None
    
    def __post_init__(self):
        if self.seed is not None:
            np.random.seed(self.seed)
        
        if self.antithetic:
            half_sim = self.n_sim // 2
            half_array = np.random.normal(loc=0.0, scale=1.0, size=(half_sim, self.n_steps, self.d))
            self.array = np.vstack((half_array, -half_array))
            if self.n_sim % 2 != 0:
                extra_array = np.random.normal(loc=0.0, scale=1.0, size=(1, self.n_steps, self.d))
                self.array = np.vstack((self.array, extra_array))
        else:
            self.array = np.random.normal(loc=0.0, scale=1.0, size=(self.n_sim, self.n_steps, self.d))
        
        # Turn first row to zeros for initial spot price
        self.array[:, 0, :] = 0.0
        return self.array

@dataclass(frozen=False)
class BasketModel(ABC):
    config: SimulationConfig
    n_underlyings: int
    basket_method: Literal['uniform', 'worst-of', 'best-of']
    paths:np.typing.NDArray

    def apply_basket_method(self):
        
        output = np.zeros_like(self.paths)

        if self.basket_method == 'uniform':
            output = np.mean(self.paths, axis=2)
        elif self.basket_method == 'worst-of':
            output = np.min(self.paths, axis=2)
        elif self.basket_method == 'best-of':
            output = np.max(self.paths, axis=2)
        else:
            raise ValueError("Invalid basket_method. Choose from 'uniform', 'worst-of', or 'best-of'.")
        return output