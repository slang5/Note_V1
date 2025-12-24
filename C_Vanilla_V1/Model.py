
from typing import Union
from datetime import date

from numpy import typing, float64, where

from C_Vanilla_V1.Option import Digital_Option, Option_Call, Option_Put, Digital_Call, Digital_Put
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
    
    @staticmethod
    def price_one_path(one_path: typing.NDArray[float64], option: Union[Option_Call, Option_Put, Digital_Call, Digital_Put], spot: Union[float, float64]) -> dict[str, Union[float, float64]]:
        
        strike = option.strike_price
        rebate = 0.0
        payout = 0.0

        price_mean: Union[float, float64] 
        price_std: Union[float, float64]

        if option.value_method == 'absolute':
            strike_value = strike
            rebate = option.rebate

            if isinstance(option, Digital_Option):
                payout = option.payout
    
        elif option.value_method == 'relative':
            strike_value = strike * spot
            rebate = option.rebate * spot

            if isinstance(option, Digital_Option):
                payout = option.payout * spot

        if option.option_type == 'EU':
            if isinstance(option, Option_Call):

                one_path_final = where(one_path > strike_value, one_path - strike_value, rebate)
                price_mean = one_path_final.mean()
                price_std = one_path_final.std()
                
            if isinstance(option, Option_Put):

                one_path_final = where(one_path < strike_value, strike_value - one_path, rebate)
                price_mean = one_path_final.mean()
                price_std = one_path_final.std()

            if isinstance(option, Digital_Call):

                one_path_final = where(one_path > strike_value, payout, rebate)
                price_mean = one_path_final.mean()
                price_std = one_path_final.std()
            
            if isinstance(option, Digital_Put):

                one_path_final = where(one_path < strike_value, payout, rebate)
                price_mean = one_path_final.mean()
                price_std = one_path_final.std()

        elif option.option_type == 'US':
            raise NotImplementedError("American option pricing not implemented yet.")

        price = price_mean
        std = price_std
        return {"price": price, "std": std}

    def price(self, spot: float = 1.0) -> dict:
        
        pricing_dict: dict[date, dict[str, Union[float, float64]]] = {}

        dates_i = 0
        for path in self.reduce_to_strike_dates().T:
            price_std = self.price_one_path(path, self.option, spot)
            pricing_dict[self.strikes_dates[dates_i]] = price_std
            dates_i += 1

        return pricing_dict

        