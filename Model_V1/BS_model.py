from base import SimulationConfig, PathBlock
from timegrid import Calendar

from datetime import date
from dataclasses import dataclass
import numpy as np

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
            n_steps=self.calendar.n_steps,
            d=len(self.underlyings),
            seed=self.seed
        )
        self.Paths.__post_init__()

    def apply_bs_formula(self):
        spots = np.array([params.spot for params in self.underlyings.values()])  # shape (d,)
        vols = np.array([params.vol for params in self.underlyings.values()])    # shape (d,)
        rates = np.array([params.rate for params in self.underlyings.values()])  # shape (d,)
        divs = np.array([params.div for params in self.underlyings.values()])    # shape (d,)

        log_spots = np.log(spots)                                              # shape (d,)

        drifts = rates - divs - 0.5 * vols ** 2                                 # shape (d,)
        dt_array = self.calendar.get_time_dt                                    # shape (n_steps,)

        Z = self.Paths.array            
        Z = np.outer(dt_array, drifts) + np.outer(np.sqrt(dt_array), vols) * Z                                  
        
        log_paths = log_spots + np.cumsum(Z, axis=1)         # shape (n_sim, n_steps, d)
        paths = np.exp(log_paths)  # shape (n_sim, n_steps, d)

        return paths

Calendar = Calendar(
    start_date = date(2024, 1, 1),
    end_date = date(2025, 12, 31),
    n_steps = 100
)

config = SimulationConfig(calendar=Calendar, n_paths=50, seed=42)
Eq1 = UnderlyingParams(isin="00001", spot=100.0, vol=0.2, rate=0.05, div=0.02)
Eq2 = UnderlyingParams(isin="00002", spot=150.0, vol=0.25, rate=0.04, div=0.03)
Eq3 = UnderlyingParams(isin="00003", spot=50.0, vol=0.40, rate=0.05, div=0.02)
Eq4 = UnderlyingParams(isin="00004", spot=25.0, vol=0.13, rate=0.04, div=0.03)
portfolio = PortfolioParams(underlyings={"00001": Eq1, "00002": Eq2, "00003": Eq3, "00004": Eq4})

Model = BS_Model(calendar=config.calendar, n_paths=config.n_paths, seed=config.seed, antithetic=config.antithetic, underlyings=portfolio.underlyings)
print(Model.apply_bs_formula())