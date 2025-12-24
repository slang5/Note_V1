
from typing import Union
from datetime import date

from numpy import typing, float64

from C_Vanilla_V1.Option import Option_Call, Option_Put, Digital_Call, Digital_Put
from B_Model_V1.base import SimulationConfig

class Vanilla_Model:
    def __init__(self, option: Union[Option_Call, Option_Put, Digital_Call, Digital_Put], config: SimulationConfig, paths: typing.NDArray[float64], strikes_dates: list[date]):
        self.option = option
        self.paths = paths
        self.config = config
        self.strikes_dates = strikes_dates

    def update_strikes_dates(self):
        for t in range(len(self.strikes_dates)):
            nearest_date = self.config.calendar.get_nearest_time_index(self.strikes_dates[t])
            if nearest_date != self.strikes_dates[t]:
                print(f"Updating strike date from {self.strikes_dates[t]} to nearest date {nearest_date}")
                self.strikes_dates[t] = nearest_date

    def reduce_to_strike_dates(self) -> typing.NDArray[float64]:
        date_indices = [self.config.calendar.get_dates.index(d) for d in self.strikes_dates]
        reduced_paths = self.paths[:, date_indices]
        return reduced_paths