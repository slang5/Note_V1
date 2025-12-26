from dataclasses import dataclass

import numpy as np

from B_Model_V1.base import SimulationConfig, PathBlock

accuracy_float = 6

@dataclass(frozen=True)
class UnderlyingParams:
    isin: str
    spot: float # current spot price 
    vol: float # annualized volatility %
    rate: float # annualized risk-free rate %
    div: float # annualized dividend yield %

    def __post_init__(self):
        if self.spot <= 0:
            raise ValueError("Spot price must be positive.")
        if self.vol < 0:
            raise ValueError("Volatility cannot be negative.")
        if not (-1.0 <= self.rate <= 1.0):
            raise ValueError("Interest rate must be between -100% and 100%.")
        if not (-1.0 <= self.div <= 1.0):
            raise ValueError("Dividend yield must be between -100% and 100%.")

@dataclass(frozen=False)
class PortfolioParams:
    underlyings: dict[str, UnderlyingParams]

    def __post_init__(self):
        if len(self.underlyings) == 0:
            raise ValueError("Portfolio must contain at least one underlying.")

@dataclass(frozen=False)
class BS_Model(SimulationConfig, PortfolioParams):
    
    def __post_init__(self):
        SimulationConfig.__post_init__(self)
        PortfolioParams.__post_init__(self)
        self.Paths = PathBlock(
            n_sim=self.n_paths,
            n_steps=self.calendar.n_steps, #type: ignore
            d=len(self.underlyings),
            antithetic=self.antithetic,
            seed=self.seed
        )

    def apply_bs_value(self):
        spots = np.array([params.spot for params in self.underlyings.values()])
        vols = np.array([params.vol for params in self.underlyings.values()])
        rates = np.array([params.rate for params in self.underlyings.values()])
        divs = np.array([params.div for params in self.underlyings.values()])

        log_spots = np.log(spots)

        drifts = rates - divs - 0.5 * vols ** 2
        dt_array = self.calendar.get_time_dt

        Z = self.Paths.array
        Z = np.outer(dt_array, drifts) + np.outer(np.sqrt(dt_array), vols) * Z
        
        log_paths = log_spots + np.cumsum(Z, axis=1)
        paths = np.exp(log_paths)

        paths = np.round(paths, accuracy_float)

        return paths
    
    def apply_bs_percentage(self):
        spots = np.array([params.spot for params in self.underlyings.values()])
        vols = np.array([params.vol for params in self.underlyings.values()])
        rates = np.array([params.rate for params in self.underlyings.values()])
        divs = np.array([params.div for params in self.underlyings.values()])

        log_spots = np.log(spots)

        drifts = rates - divs - 0.5 * vols ** 2
        dt_array = self.calendar.get_time_dt

        Z = self.Paths.array
        Z = np.outer(dt_array, drifts) + np.outer(np.sqrt(dt_array), vols) * Z
        
        paths = np.cumsum(Z, axis=1)

        paths = np.round(paths, accuracy_float)

        return np.exp(paths)
