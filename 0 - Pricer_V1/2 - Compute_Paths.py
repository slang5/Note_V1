from os import name
from sys import path
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path.insert(0, str(ROOT))

from datetime import date
import time

from B_Model_V1.bs_model import BS_Model, UnderlyingParams, PortfolioParams
from B_Model_V1.timegrid import Calendar
from B_Model_V1.base import SimulationConfig, BasketModel

Equity_1 = UnderlyingParams(
    isin="FR0000131104",
    spot=50.0,
    vol=0.2,
    rate=0.01,
    div=0.03
)

Equity_2 = UnderlyingParams(
    isin="FR0000130809",
    spot=100.0,
    vol=0.2,
    rate=0.01,
    div=0.03
)

Equity_3 = UnderlyingParams(
    isin="FR0000121014",
    spot=150.0,
    vol=0.2,
    rate=0.01,
    div=0.03
)

portfolio = PortfolioParams(
    underlyings={
        Equity_1.isin: Equity_1,
        Equity_2.isin: Equity_2,
        Equity_3.isin: Equity_3}
)

start_date = date(2010, 1, 1)
end_date = date(2011, 1, 1)
basket_method = "uniform"

Calendar_Config = Calendar(
    start_date=start_date,
    end_date=end_date,
    n_steps=2,
    trading_days=365.0
)

Sim_Config = SimulationConfig(
    calendar=Calendar_Config,
    n_paths=1_000_000,
    seed=42,
    antithetic=True
)

BS = BS_Model(
    underlyings=portfolio.underlyings,
    calendar=Sim_Config.calendar,
    n_paths=Sim_Config.n_paths,
    seed=Sim_Config.seed,
    antithetic=Sim_Config.antithetic
) 

start = time.time()

Paths = BS.apply_bs_percentage()

Basket = BasketModel(
    config=Sim_Config,
    n_underlyings=len(portfolio.underlyings),
    basket_method=basket_method,
    paths=Paths,
)

Basket_paths = Basket.apply_basket_method()
print(f"Paths array shape: {Basket_paths.shape}")

n_shown_paths = 5
print(f"Showing first {n_shown_paths} paths of the basket:")
print(f"dates : {Calendar_Config.get_dates}")

for i in range(n_shown_paths):
    print(f"Path {i+1}: {Basket_paths[i]}")


end = time.time()
print(f"Computation Time: {end - start} seconds")