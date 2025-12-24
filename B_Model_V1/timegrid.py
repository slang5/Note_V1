from dataclasses import dataclass
from typing import Optional

from datetime import date, timedelta
from numpy import diff, array, insert
from numpy.typing import NDArray

@dataclass(frozen=False)
class Calendar:
    
    start_date: date 
    end_date: date
    dt: Optional[float] = None
    n_steps: Optional[int] = None
    trading_days: float = 365.0

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
        tmp = [self.start_date + timedelta(days=int(t * (self.end_date - self.start_date).days)) for t in self.times]
        tmp = list(set(tmp))
        return sorted(tmp)

    @property
    def get_time_dt(self) -> NDArray:
        dt = diff(array(self.get_dates)).astype('timedelta64[D]').astype(float) / self.trading_days
        dt = insert(dt, 0, 0.0)
        return dt
    
    def get_nearest_time_index(self, D: date) -> date:
        date_list = self.get_dates
        nearest_date = min(date_list, key=lambda d: abs(d - D))
        return nearest_date