
from typing import Union, Literal
from datetime import date

from numpy import typing, float64, where, round

from C_Vanilla_V1.Option import Digital_Option, Option_Call, Option_Put, Digital_Call, Digital_Put
from C_Vanilla_V1.Barrier import Barrier_Feature
from B_Model_V1.base import SimulationConfig

accuracy_float = 6

class Vanilla_Model:
    def __init__(self, option: Union[Option_Call, Option_Put, Digital_Call, Digital_Put], config: SimulationConfig, paths: typing.NDArray[float64], strikes_dates: list[date]):
        self.option = option
        self.paths = round(paths, accuracy_float)
        self.config = config
        self.strikes_dates = strikes_dates

    def update_strikes_dates(self):
        for t in range(len(self.strikes_dates)):
            nearest_date = self.config.calendar.get_nearest_time_index(self.strikes_dates[t])
            if nearest_date != self.strikes_dates[t]:
                print(f"Updating strike date from {self.strikes_dates[t]} to nearest date {nearest_date}")
                self.strikes_dates[t] = nearest_date

    def reduce_to_strike_dates(self) -> typing.NDArray[float64]:
        if len(self.strikes_dates) == 0:
            raise ValueError("No strike dates provided.")    
        
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
                levier = option.levier
                one_path_final = where(one_path > strike_value, levier * (one_path - strike_value), rebate)
                price_mean = one_path_final.mean()
                price_std = one_path_final.std()
                
            if isinstance(option, Option_Put):
                levier = option.levier
                one_path_final = where(one_path < strike_value, levier * (strike_value - one_path), rebate)
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

class Barrier_Model:
    def __init__(self, barrier_feature: Barrier_Feature, config: SimulationConfig, paths: typing.NDArray[float64]):
        self.barrier_feature = barrier_feature
        self.config = config
        self.paths = round(paths, accuracy_float)
        
        self.level: float64

    def levels(self):
        spot = self.barrier_feature.spot_price
        method = self.barrier_feature.value_method
        barrier_level = self.barrier_feature.barrier_level

        self.level = round(float64(barrier_level), accuracy_float)

        return self.level
    
    def observe(self):

        value_if_activated:int = 1
        value_if_not_activated:int = 0
        tmp_array = self.barrier_feature.reduce_to_strike_dates(self.paths)

        if self.barrier_feature.barrier_mecanism in ['U&I']:
            observed = where(tmp_array >= self.levels(), value_if_activated, value_if_not_activated)

        elif self.barrier_feature.barrier_mecanism in ['U&O']:
            observed = where(tmp_array >= self.levels(), value_if_not_activated ,value_if_activated)

        elif self.barrier_feature.barrier_mecanism in ['D&I']:    
            observed = where(tmp_array <= self.levels(), value_if_activated, value_if_not_activated)

        elif self.barrier_feature.barrier_mecanism in ['D&O']:
            observed = where(tmp_array <= self.levels(), value_if_not_activated ,value_if_activated)

        return observed
    
    def apply_observe_method(self, method_obs: Literal["Best", "Worst", "Last", "First", "Above_Mean"]):

        observations = self.observe()

        if method_obs == "Best":
            results = observations.max(axis=1)
        elif method_obs == "Worst":
            results = observations.min(axis=1)
        elif method_obs == "Last":
            results = observations[:,-1]
        elif method_obs == "First":
            results = observations[:,0]
        elif method_obs == "Above_Mean":
            mean_obs = observations.mean(axis=1)
            results = where(mean_obs >= 0.5, 1, 0)

        return results.reshape((results.shape[0], 1))
    
class Vanilla_Barrier_Model:
    def __init__(self, option: Union[Option_Call, Option_Put, Digital_Call, Digital_Put], barrier_feature: Barrier_Feature, config: SimulationConfig, paths: typing.NDArray[float64], strikes_dates: list[date], barrier_method: Literal["Best", "Worst", "Last", "First", "Above_Mean"]):
        
        self.Sim_config = config
        
        self.option = option
        self.barrier = barrier_feature
        self.barrier_method = barrier_method

        self.strikes_dates = strikes_dates
        self.paths = round(paths, accuracy_float)
        
    
    
