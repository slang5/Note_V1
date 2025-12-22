from dataclasses import dataclass
from typing import Optional

from datetime import date, timedelta
from numpy import diff
from numpy.typing import NDArray

@dataclass(frozen=False)
class Calendar:
    
    start_date: date 
    end_date: date
    dt: Optional[float] = None
    n_steps: Optional[int] = None
    trading_days: float = 252.0

    def __post_init__(self):
        if self.dt is not None and self.n_steps is not None:
            raise ValueError("Only one of 'dt' or 'n_steps' should be provided.")
        if self.dt is None and self.n_steps is None:
            raise ValueError("One of 'dt' or 'n_steps' must be provided.")

        if self.dt is not None:
            self.n_steps = int(1 / self.dt) + 1
            self.times = [i * self.dt for i in range(self.n_steps)]

        elif self.n_steps is not None:
            self.n_steps = self.n_steps + 1
            self.dt = 1 / (self.n_steps - 1)
            self.times = [i * self.dt for i in range(self.n_steps)]
        else:
            raise ValueError("One of 'dt' or 'n_steps' must be provided.")
        
    @property
    def get_dates(self):
        return [self.start_date + timedelta(days=int(t * self.trading_days)) for t in self.times]
    
    