
from datetime import date
from typing import Union, Literal
from numpy import typing, float64

from B_Model_V1.timegrid import Calendar

barrier_mecanism = ['U&I', 'U&O', 'D&I', 'D&O']
barrier_exercise = ['EU', 'US']

class Barrier_Feature():
    def __init__(self, start_date: date, end_date: date, barrier_mecanism: Literal['U&I', 'U&O', 'D&I', 'D&O'], barrier_exercise: Literal['EU', 'US'], barrier_level: float, spot_price: float, value_method: Literal['absolute', 'relative'], paths: typing.NDArray[float64], observation_dates: Union[list[date], None], calendar: Union[Calendar, None] = None):
        self.start_date: date = start_date
        self.end_date: date = end_date

        self.barrier_mecanism: str = barrier_mecanism
        self.barrier_exercise: str = barrier_exercise

        self.value_method: str = value_method
        self.barrier_level: float = barrier_level
        self.spot_price: float = spot_price

        self.paths: typing.NDArray[float64] = paths

        self.observation_dates: Union[list[date], None] = observation_dates
        self.calendar: Union[Calendar, None] = calendar

        if calendar is None or observation_dates is None:
            self.calendar = None
            self.observation_dates = None
        
        else:
            self.update_observation_dates()

    def update_observation_dates(self):
        if self.calendar is None or self.observation_dates is None:
            raise ValueError("Calendar and observation_dates must be provided to update strike dates.")
        
        for t in range(len(self.observation_dates)):
            nearest_date = self.calendar.get_nearest_time_index(self.observation_dates[t])
            if nearest_date != self.observation_dates[t]:
                print(f"Updating strike date from {self.observation_dates[t]} to nearest date {nearest_date}")
                self.observation_dates[t] = nearest_date
    
    def reduce_to_strike_dates(self) -> typing.NDArray[float64]:
        if self.calendar is None or self.observation_dates is None:
            raise ValueError("Calendar and observation_dates must be provided to reduce to strike dates.")
        
        date_indices = [self.calendar.get_dates.index(d) for d in self.observation_dates]
        reduced_paths = self.paths[:, date_indices]
        return reduced_paths

    